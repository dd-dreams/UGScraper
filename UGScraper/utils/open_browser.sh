#!/bin/bash

# ARGUMENTS: 1=path, 2=browser

# there is os's which uses different names for google-chrome

CHROME="$(command -v google-chrome-stable | wc -c)"

if [ $# -gt 1 ]; then
  exec $2 $1 &> /dev/null &
  exit
fi

if [ $CHROME != "0" ]; then
    exec google-chrome-stable --incognito $1 &> /dev/null &
else
    exec google-chrome --incognito $1 &> /dev/null &
fi

