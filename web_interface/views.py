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

def pourShot(request, beverage_id):

    # less complex than an actual drink, just checking that there's liquor left
    def check_capacities(beverage_id):
        beverageObject = Beverage.objects.get(pk=beverage_id)
        return beverageObject.remaining > 35

    # same function as the drink's pour function, but duplicating here for easier logging
    def pourShot(pin, waitTime):
        print("enter pour function")
        GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has been set to LOW")
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has been set to HIGH")

    # Still going to use threading for a single thread here to keep things uniform
    def makeShot(beverageObject):

        # Start a placeholder for our threads
        pumpThreads = []

        # Log beverage being dispensed
        # TODO: encase pour function in try-catch, only log the pour if successfully completed
        beverageObject.remaining = beverageObject.remaining - 35
        beverageObject.save()

        # run the pumps as threads
        print(beverageObject.gpio_pin)
        GPIO.setup(beverageObject.gpio_pin, GPIO.OUT, initial=GPIO.HIGH)
        waitTime = 35 / beverageObject.flowrate

        pump_t = threading.Thread(target=pourShot, args=(beverageObject.gpio_pin, waitTime))
        pumpThreads.append(pump_t)

        # start the pump threads
        print(pumpThreads)
        for thread in pumpThreads:
            thread.start()
            thread.join()

    # TODO: this function should really just do everything since a single beverage, so collapse all the other ones in here
    def check_shot(request, beverage_id):
        print("checking shot capacities")
        # First, let's check that the shot exists, throwing the error page if not
        try:
            beverageObject = Beverage.objects.get(pk=beverage_id)
        except Drink.DoesNotExist:
            return render(request, 'web_interface/detail.html', {'drink': False})
        if check_capacities(beverage_id):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            makeShot(beverageObject)
            return HttpResponseRedirect('test')
        else:
             return HttpResponseRedirect('test')

    check_shot(request, beverage_id)
    return HttpResponseRedirect('/web_interface')

def pour(request, drink_id):
    print("pour triggered")
    def check_capacities(drink_id):
        print("checking capacities")
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
        print("checking drink")
        # First, let's check that the drink exists, throwing the error page if not
        try:
            drinkObject = Drink.objects.get(pk=drink_id)
        except Drink.DoesNotExist:
            return render(request, 'web_interface/detail.html', {'drink': False})
        if check_capacities(drink_id):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            makeDrink(drinkObject)
            return HttpResponseRedirect('test')
        else:
            return HttpResponseRedirect('test')
        return HttpResponseRedirect('test')

    def pour(pin, waitTime):
        print("enter pour function")
        GPIO.output(pin, GPIO.LOW)
        print("GPIO " + str(pin) + " has been set to LOW")
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)
        print("GPIO " + str(pin) + " has been set to HIGH")

    def makeDrink(drink):
        print("enter make drink function")
        # We'll start by making sure the GPIO is setup


        # Record the drink being poured
        o = Order(drink=drink, user=None)
        o.save()

        drink.total_pours = drink.total_pours + 1
        drink.save()

        # Parse the drink ingredients and spawn threads for pumps
        maxTime = 0
        pumpThreads = []
        print(drink.pour_set.all())
        for p in drink.pour_set.all():
            # Log beverage being dispensed
            p.beverage.remaining = p.beverage.remaining - p.volume
            p.beverage.save()

            # run the pumps as threads
            print(p.beverage.gpio_pin)
            GPIO.setup(p.beverage.gpio_pin, GPIO.OUT, initial=GPIO.HIGH)
            waitTime = p.volume /  p.beverage.flowrate
            if (waitTime > maxTime):
                maxTime = waitTime
            pump_t = threading.Thread(target=pour, args=(p.beverage.gpio_pin, waitTime))
            pumpThreads.append(pump_t)

        # start the pump threads
        # there seems to be an amperage issue from power supply with running all pumps in parallel
        # so we're just running threads serial until I get around to fixing it :(
        print(pumpThreads)
        for thread in pumpThreads:
            thread.start()
            thread.join()

    # Here's where we're going to actually call the functions to start the process
    check_drink(request, drink_id)
    return HttpResponseRedirect('/web_interface')

def detail(request, drink_id):
    try:
        drinkObject = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        return render(request, 'web_interface/detail.html', {'drink': False})
    return render(request, 'web_interface/detail.html', {'drink': drink_id})


