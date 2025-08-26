from django.test import TestCase
from django.urls import reverse
from .models import Trip, City, Hotel, Continent, Country
from .forms import BookingForm
from django.utils import timezone
from datetime import date, timedelta

class TripDetailViewTest(TestCase):
    def setUp(self):
        continent = Continent.objects.create(name="Evropa")
        country = Country.objects.create(name="Česká republika", continent=continent)
        origin = City.objects.create(name="Praha", country=country)
        destination = City.objects.create(name="Paříž", country=country)
        hotel = Hotel.objects.create(name="Hotel Paris", city=destination, stars=4)

        self.trip = Trip.objects.create(
            origin_city=origin,
            destination_city=destination,
            hotel=hotel,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=7),
            board_type='BB',
            price_adult=1000,
            price_child=500,
            slots_adult=5,
            slots_child=3,
            is_promoted=False
        )

    def test_trip_detail_view(self):
        url = reverse('trip_detail', kwargs={'pk': self.trip.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trip.hotel.name)

class BookingFormTest(TestCase):
    def setUp(self):
        continent = Continent.objects.create(name="Evropa")
        country = Country.objects.create(name="Česká republika", continent=continent)
        origin = City.objects.create(name="Praha", country=country)
        destination = City.objects.create(name="Paříž", country=country)
        hotel = Hotel.objects.create(name="Hotel Paris", city=destination, stars=4)

        self.trip = Trip.objects.create(
            origin_city=origin,
            destination_city=destination,
            hotel=hotel,
            departure_date=date(2025, 8, 20),
            return_date=date(2025, 8, 27),
            board_type='BB',
            price_adult=10000,
            price_child=7000,
            slots_adult=10,
            slots_child=5,
            is_promoted=False
        )

    def test_form_valid(self):
        form_data = {
            'buyer_name': 'Jana',
            'email': 'jana@example.com',
            'adults': 2,
            'children': 1
        }
        form = BookingForm(data=form_data, trip=self.trip)
        self.assertTrue(form.is_valid())

    def test_form_invalid_too_many_adults(self):
        form_data = {
            'buyer_name': 'Jana',
            'email': 'jana@example.com',
            'adults': 20,  # víc než slots_adult
            'children': 1
        }
        form = BookingForm(data=form_data, trip=self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn('adults', form.errors)

    def test_form_invalid_too_many_children(self):
        form_data = {
            'buyer_name': 'Jana',
            'email': 'jana@example.com',
            'adults': 2,
            'children': 20  # víc než slots_child
        }
        form = BookingForm(data=form_data, trip=self.trip)
        self.assertFalse(form.is_valid())
        self.assertIn('children', form.errors)