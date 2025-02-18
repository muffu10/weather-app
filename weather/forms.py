from django.forms import ModelForm, TextInput
from .models import City
import requests
from django import forms

class CityForm(ModelForm):
    class Meta:
        model=City
        fields=['name']
        widgets={'name': TextInput(attrs={'class':'input','placeholder':'City Name'})}

    def clean_name(self):
        city_name = self.cleaned_data['name']
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=52041fec7ddca2e969ffb105b6751000'
        r = requests.get(url.format(city_name)).json()
        
        if r.get('cod') != 200:  # If city is not found
            raise forms.ValidationError("Invalid city name. Please enter a valid city.")

        return city_name