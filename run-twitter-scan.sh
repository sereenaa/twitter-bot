#!/bin/bash

for i in $(cat name-list.txt) 
do
	sleep 120
	python3 check-following.py -u $i
done
