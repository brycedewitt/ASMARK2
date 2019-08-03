#!/usr/bin/env bash

## loop through each pump pin
for i in {17 27 22 23 24 25 20 21}
do
  gpio mode i out
  gpio write i 0
  sleep 3s
  gpio write i 1
done