#!/bin/bash

sudo docker rm -f jwt3
sudo docker rmi -f jwt3
sudo docker build -t jwt3 .
sudo docker run -p 1337:1337 -e FLAG=CSCCTF{FAKE_FLAG_FOR_TESTING} --name jwt3 jwt3