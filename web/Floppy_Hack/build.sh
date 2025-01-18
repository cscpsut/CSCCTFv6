#!/bin/bash

sudo docker rm -f floppy
sudo docker rmi -f floppy
sudo docker build -t floppy .
sudo docker run -p 1333:80 --name floppy -e FLAG=TESTFALAG floppy
