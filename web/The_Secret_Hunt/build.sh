#!/bin/bash

sudo docker rm -f jwt1
sudo docker rmi -f jwt1
sudo docker build -t jwt1 .
sudo docker run -p 1337:1337 --name jwt1 jwt1