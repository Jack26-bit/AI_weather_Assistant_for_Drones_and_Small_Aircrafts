"""
Tomorrow.io weather data fetching and processing module
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import Config

class TomorrowIOFetcher:
    def __init__(self):
        self.api_key = Config.TOMORROWIO_API_KEY
        self.base_url = Config.TOMORROWIO_BASE_URL
        
    def get_current_weather(self, location: str) -> Optional[Dict]:
        """
        Fetch current weather data for a specific location from Tomorrow.io
        """
        try:
            # For Tomorrow.io, we need to geocode first to get coordinates
            coords = self._geocode_location(location)
            if not coords:
                return None
                
            lat, lon = coords
            
            # Build the API request URL
            url = f"{self.base_url}/weather/realtime?location={lat},{lon}&apikey={self.api_key}&units=metric"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            # Process and structure the weather data for Tomorrow.io response
            return self._process_tomorrowio_data(data, location)
            
        except Exception as e:
            print(f"Error fetching weather data from Tomorrow.io: {e}")
            return None
    
    def get_forecast(self, location: str, days: int = 5) -> Optional[List[Dict]]:
        """
        Fetch weather forecast for the next few days from Tomorrow.io
        """
        try:
            # Geocode first to get coordinates
            coords = self._geocode_location(location)
            if not coords:
                return None
                
            lat, lon = coords
            
            # Build the API request URL
            url = f"{self.base_url}/weather/forecast?location={lat},{lon}&apikey={self.api_key}&units=metric&timesteps=1d"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            # Process the forecast data
            return self._process_forecast_data(data, days)
            
        except Exception as e:
            print(f"Error fetching forecast data from Tomorrow.io: {e}")
            return None
    
    def _geocode_location(self, location: str) -> Optional[tuple]:
        """
        Geocode a location name to coordinates using Tomorrow.io's geocoding
        """
        try:
            encoded_location = urllib.parse.quote(location)
            url = f"https://api.tomorrow.io/v4/geocode?query={encoded_location}&apikey={self.api_key}"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if data and 'features' in data and len(data['features']) > 0:
                coords = data['features'][0]['geometry']['coordinates']
                return (coords[1], coords[0])  # Return as (lat, lon)
                
            return None
            
        except Exception as e:
            print(f"Geocoding error for {location}: {e}")
            return None
    
    def _process_tomorrowio_data(self, data: Dict, location: str) -> Dict:
        """
        Process Tomorrow.io API response into our standard format
        """
        if 'data' not in data or 'time' not in data:
            raise ValueError("Invalid Tomorrow.io API response")
            
        weather_data = data['data']['values']
        
        processed = {
            'location': location,
            'coordinates': {
                'lat': data['location']['lat'],
                'lon': data['location']['lon']
            },
            'timestamp': datetime.now().isoformat(),
            'weather': {
                'main': self._get_weather_code_description(weather_data.get('weatherCode', 0)),
                'description': self._get_weather_code_description(weather_data.get('weatherCode', 0)),
                'icon': self._get_weather_icon(weather_data.get('weatherCode', 0))
            },
            'temperature': {
                'current': weather_data.get('temperature', 0),
                'feels_like': weather_data.get('temperatureApparent', 0),
                'min': weather_data.get('temperatureMin', 0),
                'max': weather_data.get('temperatureMax', 0),
                'humidity': weather_data.get('humidity', 0) * 100  # Convert from decimal to percentage
            },
            'wind': {
                'speed': weather_data.get('windSpeed', 0) * 3.6,  # Convert m/s to km/h
                'direction': weather_data.get('windDirection', 0),
                'gust': weather_data.get('windGust', 0) * 3.6 if weather_data.get('windGust') else 0
            },
            'visibility': weather_data.get('visibility', 10) / 1000,  # Convert to km
            'pressure': weather_data.get('pressureSurfaceLevel', 1013),
            'cloudiness': weather_data.get('cloudCover', 0) * 100,  # Convert from decimal to percentage
            'precipitation': {
                'rain_1h': weather_data.get('rainIntensity', 0),
                'snow_1h': weather_data.get('snowIntensity', 0)
            },
            'sunrise': '',  # Will need separate API call for these
            'sunset': ''
        }
        
        return processed
    
    def _process_forecast_data(self, data: Dict, days: int) -> List[Dict]:
        """
        Process Tomorrow.io forecast data
        """
        forecast_list = []
        
        if 'timelines' not in data or 'daily' not in data['timelines']:
            return forecast_list
            
        for day in data['timelines']['daily'][:days]:
            values = day['values']
            
            forecast_data = {
                'datetime': day['time'],
                'temperature': values.get('temperatureAvg', 0),
                'weather': self._get_weather_code_description(values.get('weatherCode', 0)),
                'wind_speed': values.get('windSpeedAvg', 0) * 3.6,  # Convert to km/h
                'wind_direction': values.get('windDirectionAvg', 0),
                'humidity': values.get('humidityAvg', 0) * 100,  # Convert to percentage
                'pressure': values.get('pressureSurfaceLevelAvg', 1013),
                'precipitation': values.get('rainIntensityAvg', 0) + values.get('snowIntensityAvg', 0),
                'cloudiness': values.get('cloudCoverAvg', 0) * 100  # Convert to percentage
            }
            
            forecast_list.append(forecast_data)
            
        return forecast_list
    
    def _get_weather_code_description(self, code: int) -> str:
        """
        Map Tomorrow.io weather codes to descriptions
        """
        weather_codes = {
            0: "Unknown",
            1000: "Clear",
            1001: "Cloudy",
            1100: "Mostly Clear",
            1101: "Partly Cloudy",
            1102: "Mostly Cloudy",
            2000: "Fog",
            2100: "Light Fog",
            3000: "Light Wind",
            3001: "Wind",
            3002: "Strong Wind",
            4000: "Drizzle",
            4001: "Rain",
            4200: "Light Rain",
            4201: "Heavy Rain",
            5000: "Snow",
            5001: "Flurries",
            5100: "Light Snow",
            5101: "Heavy Snow",
            6000: "Freezing Drizzle",
            6001: "Freezing Rain",
            6200: "Light Freezing Rain",
            6201: "Heavy Freezing Rain",
            7000: "Ice Pellets",
            7101: "Heavy Ice Pellets",
            7102: "Light Ice Pellets",
            8000: "Thunderstorm"
        }
        
        return weather_codes.get(code, "Unknown")
    
    def _get_weather_icon(self, code: int) -> str:
        """
        Map Tomorrow.io weather codes to icons
        """
        icon_map = {
            1000: "01d",  # Clear
            1001: "04d",  # Cloudy
            1100: "02d",  # Mostly Clear
            1101: "03d",  # Partly Cloudy
            1102: "04d",  # Mostly Cloudy
            2000: "50d",  # Fog
            2100: "50d",  # Light Fog
            4000: "09d",  # Drizzle
            4001: "10d",  # Rain
            4200: "09d",  # Light Rain
            4201: "10d",  # Heavy Rain
            5000: "13d",  # Snow
            5001: "13d",  # Flurries
            5100: "13d",  # Light Snow
            5101: "13d",  # Heavy Snow
            6000: "13d",  # Freezing Drizzle
            6001: "13d",  # Freezing Rain
            6200: "13d",  # Light Freezing Rain
            6201: "13d",  # Heavy Freezing Rain
            7000: "13d",  # Ice Pellets
            7101: "13d",  # Heavy Ice Pellets
            7102: "13d",  # Light Ice Pellets
            8000: "11d"   # Thunderstorm
        }
        
        return icon_map.get(code, "01d")
    
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