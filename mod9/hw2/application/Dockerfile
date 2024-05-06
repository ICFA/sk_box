FROM python:3.7.9-slim-stretch

RUN mkdir /app

COPY req.txt /app/

RUN python -m pip install -r /app/req.txt

COPY . ./

ENTRYPOINT [ "python", "app.py" ]