#!/bin/bash

# We put a password in the script
# It can be run with sudo without password, but it needs a password
# The permissions should be at max 555
# Recommended permissiones should be 500 and the server should be the owner
input=$(echo "$1" | md5sum | cut -d\  -f1)
if [ "$input" != "adf53e7c48385307d4c90dc74aedd57f" ]; then exit; fi

# If the owner is root exit
owner=$(ps x -o user 7380 | awk 'NR>1')
if [ "$owner" == "root" ]; then exit; fi

kill $2
