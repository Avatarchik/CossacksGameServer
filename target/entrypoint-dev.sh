#!/bin/bash
cd ./$scs
sed -i -E "s/chat_server   = .*/chat_server   = $HOST_NAME/" etc/simple-cossacks-server.conf
perl -mlib=lib script/simple-cossacks-server -c etc/simple-cossacks-server.conf