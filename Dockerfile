# This Dockerfile is used to build an Python environment
FROM node:18-bullseye-slim

LABEL maintainer="imgyh<admin@imgyh.com>"

WORKDIR /app

ADD . $WORKDIR

RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list

RUN apt-get update && apt-get install -y python3.9  python3-pip

RUN pip3 install -r requirements.txt

ENV TZ=Asia/Shanghai

CMD ["python3", "TikTokWeb.py"]

