#!/bin/bash

docker rm -f ribdawi-onyx:ribdawi-onyx
docker rmi -f ribdawi-onyx:ribdawi-onyx
docker build -t ribdawi-onyx:ribdawi-onyx .
