FROM python:3.7-slim
WORKDIR /usr/src/app


COPY . .
RUN apt-get update && apt-get install wget -y

## maria db 가 실행되고 나서 크롤러를 실행 하기 위한 도구
ENV DOCKERIZE_VERSION v0.6.0  
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \  
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN mkdir -p data
RUN pip3 install -r requirements.txt


RUN chmod +x docker-entrypoint.sh  
ENTRYPOINT ./docker-entrypoint.sh 

