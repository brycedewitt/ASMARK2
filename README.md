# WebPour
Web interface for a Smart Bartender's python-based command program [loosely based on this program from HackerShackOfficial](https://github.com/HackerShackOfficial/Smart-Bartender), this uses the header pins on the Raspberry Pi to control 8 hardware pumps which can mix fluids at pre-determined rates and ratios.  The Django web interface provides a way to select and trigger "pours", as well as a separate administrative interface to enter new beverages, drinks, and pump configurations.  

Implemented in Django, using MariaDB for menu storage, and running on Raspberry Pi.  

# Hardware
The current RPi hardware configuration uses BCM pins 17, 27, 22, 23, 24, 25, 20, 21 to trigger relays which switch pumps on and off.

# Configuration
As a Django application, you need to first configure a python3 virtual environment with support for Python3, Django, MySQL_Client, and RPI.GPIO.  As currently developed, this only has configurations to be locally hosted from the development server.

To setup from scratch (assuming your rpi is at 10.0.0.181 locally):
1) Install `virtualenv`
2) Configure new `virtualenv` with packages above
3) Clone and enter the repo
4) Enter database connection information in `settings.py`
5) Run local development server using `python manage.py runserver 10.0.0.181:8000`

# Management
Drinks can be configured through the Django management portal, located at `10.0.0.181/admin`.  To add new administrative user, use `python manage.py createsuperuser`.

