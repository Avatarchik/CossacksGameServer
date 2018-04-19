# This is a image of cossacks game server
FROM debian:stretch-slim
EXPOSE 34001

ARG rootpath=/app
ARG streamer=/GSC-Streamer
ARG server=/GSC-Server
ARG scs=/SimpleCossacksServer

RUN apt-get update -q --fix-missing && \
    apt-get -y upgrade && \
    apt-get -y install build-essential

ADD target/ $rootpath/

WORKDIR $rootpath

# Install perl modules via cpanm:
RUN ./bin/cpanm .$streamer/ .$server/ .$scs/

RUN $rootpath/$scs/script/simple-cossacks-server -c $rootpath/$scs/etc/simple-cossacks-server.conf
    