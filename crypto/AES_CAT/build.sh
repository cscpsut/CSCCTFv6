#!/bin/bash

sudo docker rm -f aes_cat
sudo docker rmi -f aes_cat
sudo docker build -t aes_cat .
sudo docker run -p 1337:1337 aes_cat