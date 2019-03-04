from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

import time
import sys
import RPi.GPIO as GPIO
import threading
import traceback

from .models import Beverage,Drink,Pour,User,Order

class IndexView(generic.ListView):
    template_name = 'web_interface/index.html'
    context_object_name = 'available_drinks'

    def get_queryset(self):
        """Return the last five published questions."""
        return Drink.objects.all()

def pour(request, drink_id):
    def check_drink(request, drink_id):
        # First, let's check that the drink exists, throwing the error page if not
        try:
            drinkObject = Drinks.objects.get(pk=drink_id)
        except Drink.DoesNotExist:
            return render(request, 'web_interface/invalid_drink.html', {'drink': drink_id})

        # We have a valid drink_id now, let's check if we can make it
        # Leaving this super explicit/long for debugging
        for p in drink.pour_set.all():
            needed = p.volume
            remaining = p.beverage.remaining
            if (remaining > needed):
                o = Order(drink=drinkObject)
                o.save()
                p.beverage.remaining = remaining - needed
                p.save()
        return HttpResponse("done")

    def pour(pin, waitTime):
        GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has beem set to LOW")
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has beem set to HIGH")


    def makeDrink(drink):
        # We'll start by making sure the GPIO is setup
        GPIO.setmode(GPIO.BCM)

        # Parse the drink ingredients and spawn threads for pumps
        maxTime = 0
        pumpThreads = []
        for p in drink.pour_set.all():
            GPIO.setup(p.beverage.gpio_pin, GPIO.OUT, initial=GPIO.HIGH)
            waitTime = p.volume * p.beverage.flowrate
            if (waitTime > maxTime):
                maxTime = waitTime
            pump_t = threading.Thread(target=pour, args=(p.beverage.gpio_pin, waitTime))
            pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()
        return HttpResponse("Hello, world. You're at the polls index.")

        # Here's where we're going to actually call the functions to start the process
    check_drink(request, drink_id)
