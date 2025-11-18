#!/bin/bash
echo "starting"
#let var++
#output=1
#if [[ "$var" -eq "1" ]]; then
#	echo "" > liveaddresses.txt
#fi
#echo "first loop complete"
#if [[ "$var" -eq "256" ]]; then
#	var=0
#	exit
#fi
#echo "Testing 10.10.0.$var"
#output=`ping 192.168.0."$var" -c 1 -W 0.08 | grep "ttl"`
#output=${output#*from }
#output=${output% *}
#echo test
#if [[ "$output" != "" ]]; then
#	arp -a | grep ".0.$var" >>liveaddresses.txt & arp -a | grep "$var"
#fi
#echo test
#bash newlanping.sh
#exit
function massping {
	let var++
	local output=1
	if [[ "$var" -eq "1" ]]; then
		echo "" > liveaddresses.txt
	fi
	echo "Testing 192.168.0.$var"
	local output=`ping 192.168.0."$var" -c 1 -W 0.08 | grep "ttl"`
	local output=${output#*from }
	local output=${output% *}
	echo test
	if [[ "$output" != "" ]]; then
		arp -a | grep ".0.$var" >>liveaddresses.txt & arp -a | grep "$var"
	fi
	if [[ "$var" -lt "255" ]]; then
		massping
	fi
}
var=0
massping
exit
