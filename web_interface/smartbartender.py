import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys
import RPi.GPIO as GPIO
import json
import threading
import traceback

from .models import Beverage,Drink,Pour,User,Order


def clean(self, drink):
	waitTime = 20
	pumpThreads = []

	# cancel any button presses while the drink is being made
	# self.stopInterrupts()
	self.running = True

	for p in drink.pour_set.all:
		pump_t = threading.Thread(target=self.pour, args=(p.beverage.gpio_pin, waitTime))
		pumpThreads.append(pump_t)

	# start the pump threads
	for thread in pumpThreads:
		thread.start()

	# wait for threads to finish
	for thread in pumpThreads:
		thread.join()

	# reenable interrupts
	# self.startInterrupts()
	self.running = False

def pour(self, pin, waitTime):
	GPIO.output(pin, GPIO.LOW)
    print("GPIO " + str(pin) + " has neem set to low")
	time.sleep(waitTime)
	GPIO.output(pin, GPIO.HIGH)
    print("GPIO " + str(pin) + " has neem set to low")


def makeDrink(drink):
	# cancel any button presses while the drink is being made
	# self.stopInterrupts()
	self.running = True

	# Parse the drink ingredients and spawn threads for pumps
	maxTime = 0
	pumpThreads = []
	for p in drink.pour_set.all:
				waitTime = p.volume * p.beverage.flowrate
				if (waitTime > maxTime):
					maxTime = waitTime
				pump_t = threading.Thread(target=self.pour, args=(p.beverage.gpio_pin, waitTime))
				pumpThreads.append(pump_t)

	# start the pump threads
	for thread in pumpThreads:
		thread.start()

	# wait for threads to finish
	for thread in pumpThreads:
		thread.join()

	# reenable interrupts
	# self.startInterrupts()
	self.running = False
