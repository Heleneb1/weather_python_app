from django.shortcuts import render
import urllib.request
import json
from urllib.parse import urlencode
from datetime import datetime
from decouple import config # Importer la fonction config pour lire les variables d'environnement

def index(request):
    error = False
    message = ""
    data = {}
    city = ""
    
    # Conversion de Celsius en Fahrenheit
    def celsius_to_fahrenheit(c):
        return round((c * 9 / 5) + 32, 1)
    
    # Conversion de Kelvin en Celsius
    def kelvin_to_celsius(k):
        return round(k - 273.15, 1)

    # Vérifier l'état de la conversion à partir de la requête POST
    convert = request.POST.get('convert', 'false') == 'true'  # 'false' par défaut
    temp_unit = 'F°' if convert else 'C°'  # Choisit l'unité en fonction du bouton de conversion
    
    if request.method == 'POST':
        city = request.POST.get('city', '').capitalize()  # Récupère le nom de la ville
        # Récupérer la clé API depuis .env
        api_key = config('API_KEY')
        # Récupère les données de l'API
        cityparams = {
            'q': city,
            'appid':api_key
        }
        encoded_params = urlencode(cityparams)
        url = f"http://api.openweathermap.org/data/2.5/weather?{encoded_params}"

        try:
            res = urllib.request.urlopen(url)
            json_data = json.loads(res.read())

            # Remplir les données avec la conversion en Celsius par défaut
            temp_celsius = kelvin_to_celsius(json_data['main']['temp'])
            feels_like_celsius = kelvin_to_celsius(json_data['main']['feels_like'])
            temp_min_celsius = kelvin_to_celsius(json_data['main']['temp_min'])
            temp_max_celsius = kelvin_to_celsius(json_data['main']['temp_max'])

            # Appliquer la conversion en Fahrenheit si le bouton est cliqué
            if convert:
                temp_celsius = celsius_to_fahrenheit(temp_celsius)
                feels_like_celsius = celsius_to_fahrenheit(feels_like_celsius)
                temp_min_celsius = celsius_to_fahrenheit(temp_min_celsius)
                temp_max_celsius = celsius_to_fahrenheit(temp_max_celsius)

            # Remplir le dictionnaire des données
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                "temp": f"{temp_celsius} {temp_unit}",
                "feels_like": f"{feels_like_celsius} {temp_unit}",
                "temp_min": f"{temp_min_celsius} {temp_unit}",
                "temp_max": f"{temp_max_celsius} {temp_unit}",
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
                "wind_speed": str(json_data['wind']['speed']) + ' m/s',
                "wind_deg": str(json_data['wind']['deg']),
                "cloudiness": str(json_data['clouds']['all']) + '%',
                "visibility": str(json_data['visibility']) + ' m',
                "weather_description": json_data['weather'][0]['description'],
                "sunrise": datetime.fromtimestamp(json_data['sys']['sunrise']),
                "sunset": datetime.fromtimestamp(json_data['sys']['sunset']),
                "weather_icon_url": f"http://openweathermap.org/img/wn/{json_data['weather'][0]['icon']}@2x.png"
            }
            
        except urllib.error.HTTPError as e:
            error = True
            message = "City not found. Please try another city." if e.code == 404 else f"An error occurred: {e.reason}"

    # Envoie des données et des messages d'erreur au template
    return render(request, 'index.html', {'city': city if not error else '', 'data': data, 'error': error, 'message': message, 'convert': convert})
