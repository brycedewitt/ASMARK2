from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F


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
        return Drink.availableList()
        #return Drink.objects.order_by('-total_pours')

class ShotsView(generic.ListView):
    template_name = 'web_interface/shots.html'
    context_object_name = 'available_beverages'

    def get_queryset(self):
        """Return only drinks that have enough remaining for a shot"""
        x = Beverage.objects.filter(remaining__gt=35).filter(loaded=True)
        return x.filter(drink_type__name__exact="Liquor")



class MixView(generic.ListView):
    template_name = 'web_interface/mix.html'
    context_object_name = 'available_beverages'

    def get_queryset(self):
        """Return only drinks that have enough remaining for a shot"""
        x = Beverage.objects.filter(remaining__gt=35).filter(loaded=True)
        return x.filter(drink_type__name__exact="Mix")

def pour(request, drink_id):
    def check_capacities(drink_id):
        drinkObject = Drink.objects.get(pk=drink_id)
        # We have a valid drink_id now, let's check if we can make it
        # Leaving this super explicit/long for debugging
        sufficient_remaining = 0
        number_of_pours_needed = drinkObject.pour_set.all().count()
        for p in drinkObject.pour_set.all():
            needed = p.volume
            remaining = p.beverage.remaining
            if (remaining > needed):
                sufficient_remaining += 1

        if (sufficient_remaining != number_of_pours_needed):
            return False

        for p in drinkObject.pour_set.all():
            needed = p.volume
            remaining = p.beverage.remaining
            p.beverage.remaining = remaining - needed
            p.save()
        return True

    def check_drink(request, drink_id):
        # First, let's check that the drink exists, throwing the error page if not
        try:
            drinkObject = Drink.objects.get(pk=drink_id)
        except Drink.DoesNotExist:
            return render(request, 'web_interface/detail.html', {'drink': False})
        if check_capacities(drink_id):
            makeDrink(drinkObject)
            return HttpResponseRedirect('test')
        else:
            return HttpResponseRedirect('test')
        return HttpResponseRedirect('test')

    def pour(pin, waitTime):
        #GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has been set to LOW")
        time.sleep(waitTime)
        #GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has been set to HIGH")

    def makeDrink(drink):
        # We'll start by making sure the GPIO is setup
        GPIO.setmode(GPIO.BCM)

        # Record the drink being poured
        o = Order(drink=drink, user=None)
        o.save()

        drink.total_pours = drink.total_pours + 1
        drink.save()

        # Parse the drink ingredients and spawn threads for pumps
        maxTime = 0
        pumpThreads = []
        for p in drink.pour_set.all():
            # Log beverage being dispensed
            p.beverage.remaining = p.beverage.remaining - p.volume
            p.beverage.save()

            # run the pumps as threads
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

        # cleanup GPIO
        GPIO.cleanup()


        # Here's where we're going to actually call the functions to start the process
    check_drink(request, drink_id)
    return HttpResponseRedirect('/web_interface')

def detail(request, drink_id):
    try:
        drinkObject = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        return render(request, 'web_interface/detail.html', {'drink': False})
    return render(request, 'web_interface/detail.html', {'drink': drink_id})

def pourShot(request, beverage_id):
    print('pour shot called')
    try:
        beverageObject = Beverage.objects.get(pk=beverage_id)
    except Beverage.DoesNotExist:
        return render(request, 'web_interface/detail.html', {'drink': False})
    if beverageObject.remaining > 35:
        # first, we'll log the change in quantity remaining
        beverageObject.remaining = beverageObject.remaining - 35
        beverageObject.save()

        # Setup and run the pins
        GPIO.setup(beverageObject.gpio_pin, GPIO.OUT, initial=GPIO.HIGH)
        pin = beverageObject.gpio_pin
        #GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has been set to LOW")
        time.sleep(waitTime)
        #GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has been set to HIGH")

        # cleanup GPIO
        GPIO.cleanup()
    return HttpResponseRedirect('/web_interface/shots')
