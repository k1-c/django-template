#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y

sudo apt -y install --reinstall make
sudo apt -y install curl

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh
sudo usermod -a -G docker $(whoami)
sudo service docker start

sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt -y install haveged
sudo DAEMON_ARGS="-w 1024"
sudo update-rc.d haveged defaults
