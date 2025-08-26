from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from .models import Trip, Continent, Booking, Hotel, City
from .forms import TripFilterForm, BookingForm,TripForm


class HomeView(ListView):
    model = Trip
    template_name = 'trips/home.html'
    context_object_name = 'promoted_trips'

    def get_queryset(self):
        today = timezone.now().date()
        return Trip.objects.filter(is_promoted=True, departure_date__gte=today).order_by('departure_date')[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['upcoming_trips'] = Trip.objects.filter(departure_date__gte=today).order_by('departure_date')[:3]
        continents = Continent.objects.all()
        context['continents'] = continents

        trips_by_continent = {}
        for continent in continents:
            trips_by_continent[continent.name] = Trip.objects.filter(
                destination_city__country__continent=continent
            ).order_by('departure_date')[:3]
        context['trips_by_continent'] = trips_by_continent

        context['form'] = TripFilterForm(self.request.GET or None)
        return context


class TripListView(ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        form = TripFilterForm(self.request.GET or None)
        qs = super().get_queryset()
        filter_name = "Všechny zájezdy"
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('continent'):
                qs = qs.filter(destination_city__country__continent=cd['continent'])
                filter_name = cd['continent'].name
            if cd.get('country'):
                qs = qs.filter(destination_city__country=cd['country'])
                filter_name = cd['country'].name
            if cd.get('city'):
                qs = qs.filter(destination_city=cd['city'])
                filter_name = cd['city'].name
            if cd.get('hotel'):
                qs = qs.filter(hotel=cd['hotel'])
                filter_name = cd['hotel'].name
            if cd.get('board_type'):
                qs = qs.filter(board_type=cd['board_type'])
            if cd.get('departure_date_from'):
                qs = qs.filter(departure_date__gte=cd['departure_date_from'])
            if cd.get('departure_date_to'):
                qs = qs.filter(departure_date__lte=cd['departure_date_to'])
            if cd.get('return_date_from'):
                qs = qs.filter(return_date__gte=cd['return_date_from'])
            if cd.get('return_date_to'):
                qs = qs.filter(return_date__lte=cd['return_date_to'])
        self.filter_name = filter_name
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TripFilterForm(self.request.GET or None)
        context['filter_name'] = getattr(self, 'filter_name', "Všechny zájezdy")
        return context


class TripDetailView(DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TripFilterForm(self.request.GET or None)
        return context


class TripBookingView(FormView):
    template_name = 'trips/trip_book.html'
    form_class = BookingForm
    success_url = reverse_lazy('trip_list')

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, pk=kwargs['trip_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['trip'] = self.trip
        return kwargs

    def form_valid(self, form):
        adults = form.cleaned_data['adults']
        children = form.cleaned_data['children']
        total_price = adults * self.trip.price_adult + children * self.trip.price_child

        Booking.objects.create(trip=self.trip, adults=adults, children=children, total_price=total_price)

        self.trip.slots_adult -= adults
        self.trip.slots_child -= children
        self.trip.save()

        messages.success(self.request, f"Zájezd úspěšně zakoupen! Cena celkem: {total_price} Kč")
        return redirect('trip_detail', pk=self.trip.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip'] = self.trip
        return context


class TripCreateView(CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_add.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()  # aby byly dostupné v šabloně
        return context


class HotelsByCityView(View):
    def get(self, request, city_id):
        hotels = Hotel.objects.filter(city_id=city_id).values('id', 'name')
        hotels_list = list(hotels)
        return JsonResponse(hotels_list, safe=False)