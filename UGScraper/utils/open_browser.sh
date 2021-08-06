#!/bin/sh

# ARGUMENTS: 1=path, 2=browser


# checking if specified browser

echo $1

[ $# -gt 1 ] && $($2 $1 &> /dev/null &) && exit

# you gotta make sure you set BROWSER env variable to your preferred browser (can be any one)
[ $# = 1 ] && $BROWSER $1 --incognito &> /dev/null &

