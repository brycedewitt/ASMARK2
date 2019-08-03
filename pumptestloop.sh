#!/usr/bin/env bash

17 27 22 23 24 25 20 21

## loop through each pump pin
for i in 17 27 22 23 24 25 20 21
do
  echo "working on pin $i"
  gpio -g mode $i out
  gpio -g write $i 0
  sleep 2s
  gpio -g write $i 1
done