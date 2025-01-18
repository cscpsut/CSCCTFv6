#!/bin/bash
sudo docker rm -f csc-24-calc
sudo docker rmi -f csc-24-calc
sudo docker build -t csc-24-calc .
sudo docker run -d -p 1337:1337 --name csc-24-calc csc-24-calc
