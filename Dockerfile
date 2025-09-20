FROM python:3.13-slim-bookworm

ADD aria2-proxy.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "aria2-proxy.py" ]
