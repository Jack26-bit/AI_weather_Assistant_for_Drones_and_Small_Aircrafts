"""
Weather data fetching and processing module - WebContainer compatible version
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import Config

class WeatherFetcher:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        
    def get_current_weather(self, location: str) -> Optional[Dict]:
        """
        Fetch current weather data for a specific location
        """
        try:
            # URL encode the location parameter
            encoded_location = urllib.parse.quote(location)
            url = f"{self.base_url}/weather?q={encoded_location}&appid={self.api_key}&units=metric"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            # Process and structure the weather data
            weather_data = {
                'location': f"{data['name']}, {data['sys']['country']}",
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                },
                'timestamp': datetime.now().isoformat(),
                'weather': {
                    'main': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                },
                'temperature': {
                    'current': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'min': data['main']['temp_min'],
                    'max': data['main']['temp_max'],
                    'humidity': data['main']['humidity']
                },
                'wind': {
                    'speed': data.get('wind', {}).get('speed', 0) * 3.6,  # Convert m/s to km/h
                    'direction': data.get('wind', {}).get('deg', 0),
                    'gust': data.get('wind', {}).get('gust', 0) * 3.6 if data.get('wind', {}).get('gust') else 0
                },
                'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
                'pressure': data['main']['pressure'],
                'cloudiness': data['clouds']['all'],
                'precipitation': {
                    'rain_1h': data.get('rain', {}).get('1h', 0),
                    'snow_1h': data.get('snow', {}).get('1h', 0)
                },
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            }
            
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_forecast(self, location: str, days: int = 5) -> Optional[List[Dict]]:
        """
        Fetch weather forecast for the next few days
        """
        try:
            encoded_location = urllib.parse.quote(location)
            url = f"{self.base_url}/forecast?q={encoded_location}&appid={self.api_key}&units=metric"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            forecast_list = []
            
            for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                forecast_data = {
                    'datetime': datetime.fromtimestamp(item['dt']).isoformat(),
                    'temperature': item['main']['temp'],
                    'weather': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'] * 3.6,  # Convert to km/h
                    'wind_direction': item['wind']['deg'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'precipitation': item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0),
                    'cloudiness': item['clouds']['all']
                }
                forecast_list.append(forecast_data)
            
            return forecast_list
            
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
            return None
    
    def get_multiple_locations(self, locations: List[str]) -> Dict[str, Dict]:
        """
        Fetch weather data for multiple locations
        """
        weather_data = {}
        
        for location in locations:
            data = self.get_current_weather(location)
            if data:
                weather_data[location] = data
            
        return weather_data