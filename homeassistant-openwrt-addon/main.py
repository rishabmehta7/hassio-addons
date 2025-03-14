import yaml
import paramiko
import requests
from fastapi import FastAPI

app = FastAPI()

# Load routers from the config file
with open("/data/options.json", "r") as file:
    config = yaml.safe_load(file)
routers = config.get("routers", [])

def send_ssh_command(ip, username, password, command):
    """Execute SSH command on OpenWRT router."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        client.close()
        return output
    except Exception as e:
        return str(e)

@app.get("/routers")
def list_routers():
    """List available routers"""
    return {"routers": routers}

@app.post("/execute")
def execute_command(router_name: str, command: str):
    """Execute a command on a router"""
    router = next((r for r in routers if r["name"] == router_name), None)
    if not router:
        return {"error": "Router not found"}
    
    result = send_ssh_command(router["ip"], router["username"], router["password"], command)
    return {"router": router_name, "output": result}

@app.get("/status")
def get_status():
    """Get router status (CPU, RAM, uptime)"""
    status_data = {}
    for router in routers:
        result = send_ssh_command(router["ip"], router["username"], router["password"], "ubus call system board")
        status_data[router["name"]] = result
    return status_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
