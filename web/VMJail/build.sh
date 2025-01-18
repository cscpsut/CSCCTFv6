#!/bin/bash

sudo docker rmi -f web-vmjail
sudo docker build -t web-vmjail .
sudo docker run -p 3000:3000 web-vmjail