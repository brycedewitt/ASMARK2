#!/usr/bin/env bash

## loop through each pump pin
for i in {17 27 22 23 24 25 20 21}
do
  gpio mode i out
  gpio set i 0
  sleep 3s
  gpio set i 1
done