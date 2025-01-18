#!/bin/bash

sudo docker rm -f misc-windows
sudo docker rmi -f misc-windows
sudo docker build -t misc-windows .
sudo docker run -p 1337:1337 --name misc-windows misc-windows