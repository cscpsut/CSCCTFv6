#!/bin/bash
sudo docker rm -f initial_breach
sudo docker rmi -f initial_breach
sudo docker build -t initial_breach .
sudo docker run -p 1337:1337 --rm -e FLAG=CSCCTF{FAKE_FALG_FOR_TESTING} initial_breach