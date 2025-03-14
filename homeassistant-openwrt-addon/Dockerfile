FROM ghcr.io/home-assistant/amd64-base:latest

RUN apk add --no-cache python3 py3-pip openssh-client

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY main.py /main.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
