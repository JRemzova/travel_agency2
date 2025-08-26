from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class Continent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField()
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.stars}★)"

class Trip(models.Model):
    origin_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trips_from')
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trips_to')
    hotel = ChainedForeignKey(
        Hotel,
        chained_field="destination_city",
        chained_model_field="city",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
    )
    departure_date = models.DateField()
    return_date = models.DateField()
    board_type = models.CharField(max_length=2, choices=[('BB','Bed & Breakfast'),('HB','Half Board'),('FB','Full Board'),('AI','All Inclusive')])
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2)
    slots_adult = models.IntegerField()
    slots_child = models.IntegerField()
    is_promoted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.destination_city.name} - {self.hotel.name} ({self.departure_date})"
    @property
    def duration_days(self):
        return (self.return_date - self.departure_date).days

class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    buyer_name = models.CharField(max_length=50)
    email = models.EmailField()
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.trip} - Adults: {self.adults}, Children: {self.children}"