#!/bin/bash

sudo docker rm -f jwt2
sudo docker rmi -f jwt2
sudo docker build -t jwt2 .
sudo docker run -p 1337:1337 --name jwt2 jwt2