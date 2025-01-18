#!/bin/bash
sudo docker rm -f final
sudo docker rmi -f final
sudo docker build -t final .
sudo docker run -p 1337:1337 --rm -e FLAG=CSCCTF{FAKE_FALG_FOR_TESTING} final