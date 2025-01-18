#!/bin/bash

sudo docker rm -f web-mindsweeper
sudo docker rmi -f web-mindsweeper
sudo docker build -t web-mindsweeper .
sudo docker run -p 1337:1337 --name web-mindsweeper web-mindsweeper