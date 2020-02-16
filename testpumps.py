#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [17, 27, 22, 23, 24, 25, 20, 21]

for i in pins:
	print('Checking pin ' + str(i))
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, 0)
	time.sleep(1)
	GPIO.output(i, 1)

GPIO.cleanup()
