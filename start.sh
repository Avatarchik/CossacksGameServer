#!/bin/bash

if [ ! -f .env ]; then
    printf "Irc server name not found\nCreating new one: "
    hostname=irc.$(openssl rand -hex 32 | fold -w 9 | head -n 1).com
    echo $hostname
    echo "HOST_NAME=$hostname" > .env
fi
docker-compose up --build "$@"