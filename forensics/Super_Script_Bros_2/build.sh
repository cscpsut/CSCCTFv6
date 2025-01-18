#!/bin/bash
sudo docker rm -f privesc
sudo docker rmi -f privesc
sudo docker build -t privesc .
sudo docker run -p 1337:1337 --rm -e FLAG=CSCCTF{FAKE_FALG_FOR_TESTING} privesc