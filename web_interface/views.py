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

    drink = get_object_or_404(Drink, pk=drink_id)

    GPIO.setmode(GPIO.BCM)



    def pour(pin, waitTime):
        GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has beem set to LOW")
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has beem set to HIGH")


    def makeDrink(drink):

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


    print(Drink.objects.get(pk=drink_id).pour_set.all())
    makeDrink(Drink.objects.get(pk=drink_id))
    return HttpResponse("Hello, world. You're at the polls index.")
