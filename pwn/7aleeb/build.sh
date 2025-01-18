#!/bin/bash

docker rm -f 7aleeb:7aleeb
docker rmi -f 7aleeb:7aleeb
docker build -t 7aleeb:7aleeb .
