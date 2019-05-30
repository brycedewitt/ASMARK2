from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    venmo = models.CharField(max_length=200)
    swipecode = models.CharField(max_length=400, default='none')
    pin = models.PositiveIntegerField(unique=True, null=False, validators=[MaxValueValidator(999999)])
    register_date = models.DateTimeField(default=now)
    total_drinks = models.IntegerField(default=0)
    credit = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["total_drinks"]
        verbose_name_plural = 'Users'

class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    total_pours = models.IntegerField(default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=1.99)
    created_date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def pourTime(self):
        maxTime = 0
        for p in self.pour_set.all():
            prevTime = maxTime
            waitTime = p.volume * p.beverage.flowrate
            maxTime = prevTime + waitTime + 3

        print(maxTime)
        return maxTime

    def availableList():
        ids = []
        for d in Drink.objects.all():
            if Drink.allLoaded(d):
                ids.append(d.id)
        return Drink.objects.all().filter(id__in=ids).order_by('-total_pours')

    def allLoaded(self):
        x = self.pour_set.all().count()
        y = 0
        for p in self.pour_set.all():
            if p.beverage.loaded:
                y += 1
        return (x==y)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["total_pours"]
        verbose_name_plural = 'Drinks'

class DrinkType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Drink Types'

class Beverage(models.Model):
    name = models.CharField(max_length=200)
    loaded = models.BooleanField(default=False)
    capacity = models.IntegerField(default=1000)
    remaining = models.IntegerField(default=500)
    drink_type = models.ForeignKey(DrinkType, on_delete=models.CASCADE, null=True)
    cost_per_unit = models.DecimalField(decimal_places=4, max_digits=10, default=0.5900)
    gpio_pin = models.IntegerField(null=False, unique=True)
    flowrate = models.DecimalField(decimal_places=4, max_digits=10, default=0.5900)

    def shot_cost(self):
        return float('%.2f'%(self.cost_per_unit * 35))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Beverages'

class Pour(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    volume = models.IntegerField(default=20)

    def __str__(self):
        x = str(self.drink)
        y = str(self.beverage)
        z = str(self.volume)
        out = x + ' -- ' + z + 'ml of ' + y
        return out

    class Meta:
        ordering = ["-volume"]
        verbose_name_plural = 'Pours'


class Order(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        drink = str(self.drink)
        user = str(self.user)
        timestamp = str(self.timestamp)
        out = user + ' -- ' + drink + ' at ' + timestamp
        return out

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = 'Orders'
