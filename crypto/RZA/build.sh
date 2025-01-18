#!/bin/bash
sudo docker rm -f rza
sudo docker rmi -f rza
sudo docker build -t rza .
sudo docker run -p 1337:1337  rza