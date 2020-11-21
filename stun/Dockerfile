# This is a image of cossacks stun server
FROM alpine:latest

ENV rootpath /app

RUN apk update && \
    apk add python3

RUN python3 -m ensurepip

ADD target/ $rootpath/

WORKDIR $rootpath

RUN pip3 install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]