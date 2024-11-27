FROM python:3.9-alpine

RUN apk add --no-cache build-base libffi-dev

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /home_cloud_service
WORKDIR /home_cloud_service

ENTRYPOINT ["python", "-u", "main.py"]