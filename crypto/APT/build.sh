#!/bin/bash

sudo docker rm -f apt .
sudo docker rmi -f apt .
sudo docker build -t apt .
sudo docker run -p 1337:1337 apt 