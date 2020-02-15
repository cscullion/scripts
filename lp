#!/bin/sh
#set -x
if [ $# -eq 0 ] ; then
	echo "usage: lp <user email address>"
	exit 1
fi

status=$(lpass status | grep "Logged in")
if [ -z "$status" ] ; then
    lpass login --trust "$1"
fi
lpass ls > /tmp/lp.txt
name=$(cat /tmp/lp.txt | grep -F '[' | awk -F[ '{print $1}' | dmenu)
if [ -n "$name" ] ; then
    id=$(cat /tmp/lp.txt | grep "$name" | awk -F 'id: ' '{print $2}' | tr -d "]")
    for idn in $id
    do
        lpass show --username "$idn"
        lpass show --password "$idn" | xclip -f -r -selection clipboard
        echo -e ''
    done
fi
rm /tmp/lp.txt
