FROM ubuntu:16.04
MAINTAINER pennymav <peny.mavroidi@gmail.com>
RUN apt-get update &&\
    apt-get install -y python3 python3-pip &&\
    pip3 install flask pymongo &&\
    apt-get install -y locales &&\
    mkdir /app &&\
    mkdir -p /app/static &&\
    mkdir -p /app/templates &&\
    locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
WORKDIR /app
COPY app.py /app/app.py

EXPOSE 5000
ENTRYPOINT [ "python3","-u","app.py" ]