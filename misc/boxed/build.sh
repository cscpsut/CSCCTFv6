#!/bin/bash

sudo docker rm -f misc-boxed
sudo docker rmi -f misc-boxed
sudo docker build -t misc-boxed .
sudo docker run -p 1337:1337 misc-boxed