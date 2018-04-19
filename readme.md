This image is compilation of next components:
1. https://github.com/envy124/SimpleCossacksServer
2. https://github.com/envy124/GSC-Server
3. https://github.com/envy124/GSC-Streamer
4. irc server

For *nix systems run start.sh and make sure that variable *HOST_NAME* in ".env" points to the right hostname(your dns hame or ip address)

INSTALLATION:
1. git clone --recurse-submodules https://github.com/envy124/CossacksGameServer; cd CossacksGameServer
2. echo "HOST_NAME=YOUR_HOSTNAME" > .env


Use "./start.sh" to run server


TODO:
* fix volumes
* make start.bat for windows
* fix server ip inside docker