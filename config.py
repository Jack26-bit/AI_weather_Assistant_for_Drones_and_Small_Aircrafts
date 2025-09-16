"""
Configuration settings for the Weather Assistant
"""
import os

class Config:
    # Tomorrow.io API configuration
    TOMORROWIO_API_KEY = os.getenv('TOMORROWIO_API_KEY', 'your_tomorrow_io_api_key_here')
    TOMORROWIO_BASE_URL = 'https://api.tomorrow.io/v4'
    
    # Flight safety thresholds
    WIND_SPEED_LIMITS = {
        'safe': 15,        # km/h
        'caution': 25,     # km/h  
        'dangerous': 35    # km/h
    }
    
    VISIBILITY_LIMITS = {
        'safe': 10,        # km
        'caution': 5,      # km
        'dangerous': 1     # km
    }
    
    TEMPERATURE_LIMITS = {
        'min_safe': -10,   # °C
        'max_safe': 40     # °C
    }
    
    # Default locations for multi-location weather
    DEFAULT_LOCATIONS = [
        'New York',
        'Los Angeles', 
        'Chicago',
        'Miami',
        'Denver'
    ]
    
    # Precipitation limits (mm/h)
    PRECIPITATION_LIMITS = {
        'light': 2.5,
        'moderate': 7.6,
        'heavy': 50
    }
    
    # Cloud cover limits (%)
    CLOUD_COVER_LIMITS = {
        'clear': 25,
        'partly_cloudy': 75,
        'overcast': 100
    }