#!/bin/bash

sudo docker rm -f xp-login
sudo docker rmi -f xp-login
sudo docker build -t xp-login .
sudo docker run -p 1337:1337 --name xp-login xp-login