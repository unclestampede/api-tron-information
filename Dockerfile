FROM python:3.11.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

COPY . /app/
WORKDIR /app

RUN apt update && apt install -y make

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["bash", "./entrypoint.sh"]
