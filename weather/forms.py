from django.forms import ModelForm, TextInput
from .models import City
import requests
from django import forms
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


class CityForm(ModelForm):
    class Meta:
        model=City
        fields=['name']
        widgets={'name': TextInput(attrs={'class':'input','placeholder':'City Name'})}

    def clean_name(self):
        city_name = self.cleaned_data['name']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={API_KEY}'
        r = requests.get(url.format(city_name)).json()
        
        if r.get('cod') != 200:  # If city is not found
            raise forms.ValidationError("Invalid city name. Please enter a valid city.")

        return city_name