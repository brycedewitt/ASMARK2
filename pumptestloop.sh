#!/usr/bin/env bash

## loop through each pump pin
for i in 17 27 22 23 24 25 20 21
do
  echo "working on pin $i"
  gpio mode $(i) out
  gpio write $(i) 0
  sleep 2s
  gpio write $(i) 1
done