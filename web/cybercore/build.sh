#!/bin/bash

sudo docker rm -f web-cybercore
sudo docker rmi -f web-cybercore
sudo docker build -t web-cybercore .
sudo docker run -p 1337:1337 web-cybercore