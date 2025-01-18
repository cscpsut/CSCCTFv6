#!/bin/bash

echo $FLAG > /flag.txt
chmod 444 /flag.txt
apache2-foreground