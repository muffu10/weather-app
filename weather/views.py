from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import City
from .forms import CityForm
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def index(request, city_name=None):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={API_KEY}'
    
    error_message = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            if City.objects.filter(name=city_name).exists():
                error_message = 'City already added!'
            else:
                form.save()  # Now only valid city names will be saved
                return redirect('city_weather', city_name=city_name)
        else:
            error_message='No Such City Exists!!'

    form = CityForm()
    cities = City.objects.all()
    weather_data = None

    if city_name:
        r = requests.get(url.format(city_name)).json()
        if r.get('cod') == 200:
            weather_data = {
                'city': city_name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']
            }

    context = {'cities': cities, 'weather_data': weather_data, 'form': form, 'error_message': error_message}
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    city=get_object_or_404(City,name=city_name)
    city.delete()
    return redirect('home')
