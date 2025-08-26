from django.contrib import admin
from .models import Continent, Country, City, Hotel, Trip, Booking

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Trip)
admin.site.register(Booking)


