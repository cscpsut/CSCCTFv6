#!/bin/bash

echo $FLAG > /flag.txt
chmod 444 /flag.txt
node /app/app.js
