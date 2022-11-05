#!/bin/bash

for i in $(cat name-list.txt) 
do
	sleep 10
	python3 check-following.py -u $i
done
