#!/bin/bash
cd ./$scs
sed -i -E "s/chat_server   = .*/chat_server   = $HOST_NAME/" etc/simple-cossacks-server.conf
sed -i "s/hole_int      = 300/hole_int      = $UDP_KEEP_ALIVE_INTERVAL/" etc/simple-cossacks-server.conf
perl -mlib=lib script/simple-cossacks-server -c etc/simple-cossacks-server.conf