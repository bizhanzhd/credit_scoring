FROM ubuntu:16.04
FROM python:3.8


RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools 

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip==22.0.4
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
