from django import forms
from .models import Continent, Country, City, Hotel, Trip

class TripFilterForm(forms.Form):
    continent = forms.ModelChoiceField(
        queryset=Continent.objects.all(),
        required=False,
        empty_label="Vyber kontinent",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Vyber zemi",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="Vyber město",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        required=False,
        empty_label="Vyber hotel",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    board_type = forms.ChoiceField(
        choices=[('', 'Vše'), ('BB', 'Bed & Breakfast'), ('HB', 'Half Board'), ('FB', 'Full Board'), ('AI', 'All Inclusive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    departure_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    departure_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    return_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    return_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

from django import forms

class BookingForm(forms.Form):
    buyer_name = forms.CharField(
        max_length=50,
        label="Jméno kupujícího",
        widget=forms.TextInput(attrs={'placeholder': 'Vaše jméno'})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'vas@email.cz'})
    )
    adults = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'value': '0', 'min': '1'})
    )
    children = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'value': '0', 'min': '0'})
    )

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        adults = cleaned_data.get('adults')
        children = cleaned_data.get('children')

        if self.trip:
            if adults and adults > self.trip.slots_adult:
                self.add_error('adults', f"Není dostatek volných míst pro dospělé (max {self.trip.slots_adult}).")
            if children and children > self.trip.slots_child:
                self.add_error('children', f"Není dostatek volných míst pro děti (max {self.trip.slots_child}).")

        return cleaned_data

class TripForm(forms.ModelForm):
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Trip
        fields = '__all__'


