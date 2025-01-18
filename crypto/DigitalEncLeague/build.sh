#!/bin/bash

sudo docker rm -f digitalencleague
sudo docker rmi -f digitalencleague
sudo docker build -t digitalencleague .
sudo docker run -p 1337:1337 digitalencleague