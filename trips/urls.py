from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import HomeView, TripListView, TripDetailView, TripBookingView, TripCreateView, HotelsByCityView
from accounts.views import user_logout, UserRegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('trips/', TripListView.as_view(), name='trip_list'),
    path('trip/<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
    path('trip/<int:trip_id>/book/', TripBookingView.as_view(), name='trip_book'),
    path('trip/add/', TripCreateView.as_view(), name='trip_add'),
    path('ajax/hotels/<int:city_id>/', HotelsByCityView.as_view(), name='hotels_by_city'),
    path("chaining/", include("smart_selects.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/register/', UserRegisterView.as_view(), name='register'),
]
