#!/bin/bash

sudo docker rm -f  shahed_zoor
sudo docker rmi -f shahed_zoor
sudo docker build -t shahed_zoor .
sudo docker run -p 1337:1337 shahed_zoor