#!/bin/bash

docker rm -f changemyname:changemyname
docker rmi -f changemyname:changemyname
docker build -t changemyname:changemyname .
