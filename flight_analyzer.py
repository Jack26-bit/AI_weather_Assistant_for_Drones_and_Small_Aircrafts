"""
Flight safety analysis based on weather conditions
"""
from typing import Dict, List, Tuple
from enum import Enum
import math
from config import Config

class FlightSafety(Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION" 
    DANGEROUS = "DANGEROUS"
    NO_FLY = "NO_FLY"

class FlightAnalyzer:
    def __init__(self):
        self.wind_limits = Config.WIND_SPEED_LIMITS
        self.visibility_limits = Config.VISIBILITY_LIMITS
        self.temp_limits = Config.TEMPERATURE_LIMITS
        self.precip_limits = Config.PRECIPITATION_LIMITS
    
    def calculate_flight_score(self, weather_data: Dict) -> Tuple[int, FlightSafety]:
        """
        Calculate a flight safety score based on weather conditions
        Returns: (score, safety_level) where score is 0-100
        """
        if not weather_data:
            return 0, FlightSafety.NO_FLY
        
        scores = []
        
        # Wind analysis (30% weight)
        wind_score = self._analyze_wind(weather_data['wind'])
        scores.append(wind_score * 0.3)
        
        # Visibility analysis (25% weight)
        visibility_score = self._analyze_visibility(weather_data['visibility'])
        scores.append(visibility_score * 0.25)
        
        # Temperature analysis (15% weight)
        temp_score = self._analyze_temperature(weather_data['temperature']['current'])
        scores.append(temp_score * 0.15)
        
        # Precipitation analysis (20% weight)
        precip_score = self._analyze_precipitation(weather_data['precipitation'])
        scores.append(precip_score * 0.20)
        
        # Cloud cover analysis (10% weight)
        cloud_score = self._analyze_clouds(weather_data['cloudiness'])
        scores.append(cloud_score * 0.10)
        
        total_score = sum(scores)
        safety_level = self._determine_safety_level(total_score)
        
        return int(total_score), safety_level
    
    def _analyze_wind(self, wind_data: Dict) -> int:
        """Analyze wind conditions (0-100 score)"""
        wind_speed = wind_data['speed']
        wind_gust = wind_data['gust']
        
        # Use the higher of wind speed or gust for safety
        effective_wind = max(wind_speed, wind_gust)
        
        if effective_wind <= self.wind_limits['safe']:
            return 100
        elif effective_wind <= self.wind_limits['caution']:
            return 70 - int((effective_wind - self.wind_limits['safe']) * 3)
        elif effective_wind <= self.wind_limits['dangerous']:
            return 40 - int((effective_wind - self.wind_limits['caution']) * 2)
        else:
            return 0
    
    def _analyze_visibility(self, visibility_km: float) -> int:
        """Analyze visibility conditions (0-100 score)"""
        if visibility_km >= self.visibility_limits['safe']:
            return 100
        elif visibility_km >= self.visibility_limits['caution']:
            return 70
        elif visibility_km >= self.visibility_limits['dangerous']:
            return 30
        else:
            return 0
    
    def _analyze_temperature(self, temperature: float) -> int:
        """Analyze temperature conditions (0-100 score)"""
        if self.temp_limits['min_safe'] <= temperature <= self.temp_limits['max_safe']:
            return 100
        elif temperature < self.temp_limits['min_safe']:
            # Cold temperature penalty
            diff = self.temp_limits['min_safe'] - temperature
            return max(0, 100 - diff * 5)
        else:
            # Hot temperature penalty
            diff = temperature - self.temp_limits['max_safe']
            return max(0, 100 - diff * 3)
    
    def _analyze_precipitation(self, precip_data: Dict) -> int:
        """Analyze precipitation conditions (0-100 score)"""
        total_precip = precip_data['rain_1h'] + precip_data['snow_1h']
        
        if total_precip == 0:
            return 100
        elif total_precip <= self.precip_limits['light']:
            return 80
        elif total_precip <= self.precip_limits['moderate']:
            return 50
        elif total_precip <= self.precip_limits['heavy']:
            return 20
        else:
            return 0
    
    def _analyze_clouds(self, cloudiness: int) -> int:
        """Analyze cloud cover (0-100 score)"""
        if cloudiness <= 25:
            return 100  # Clear skies
        elif cloudiness <= 50:
            return 85   # Partly cloudy
        elif cloudiness <= 75:
            return 70   # Mostly cloudy
        else:
            return 50   # Overcast
    
    def _determine_safety_level(self, score: float) -> FlightSafety:
        """Determine safety level based on overall score"""
        if score >= 80:
            return FlightSafety.SAFE
        elif score >= 60:
            return FlightSafety.CAUTION
        elif score >= 30:
            return FlightSafety.DANGEROUS
        else:
            return FlightSafety.NO_FLY
    
    def generate_flight_recommendations(self, weather_data: Dict, score: int, safety_level: FlightSafety) -> List[str]:
        """Generate specific flight recommendations based on weather analysis"""
        recommendations = []
        
        # Wind recommendations
        wind_speed = weather_data['wind']['speed']
        if wind_speed > self.wind_limits['caution']:
            recommendations.append(f"⚠️ High wind speeds ({wind_speed:.1f} km/h). Consider postponing flight.")
        elif wind_speed > self.wind_limits['safe']:
            recommendations.append(f"🌪️ Moderate winds ({wind_speed:.1f} km/h). Experienced pilots only.")
        
        # Visibility recommendations
        visibility = weather_data['visibility']
        if visibility < self.visibility_limits['caution']:
            recommendations.append(f"🌫️ Low visibility ({visibility:.1f} km). Use visual observers.")
        
        # Temperature recommendations
        temp = weather_data['temperature']['current']
        if temp < self.temp_limits['min_safe']:
            recommendations.append(f"🥶 Cold temperature ({temp:.1f}°C). Check battery performance.")
        elif temp > self.temp_limits['max_safe']:
            recommendations.append(f"🌡️ High temperature ({temp:.1f}°C). Monitor for overheating.")
        
        # Precipitation recommendations
        rain = weather_data['precipitation']['rain_1h']
        snow = weather_data['precipitation']['snow_1h']
        if rain > 0:
            recommendations.append(f"🌧️ Rain detected ({rain:.1f}mm/h). Protect equipment from moisture.")
        if snow > 0:
            recommendations.append(f"❄️ Snow detected ({snow:.1f}mm/h). Cold weather precautions advised.")
        
        # General safety recommendations based on level
        if safety_level == FlightSafety.SAFE:
            recommendations.append("✅ Conditions are favorable for flight operations.")
        elif safety_level == FlightSafety.CAUTION:
            recommendations.append("⚠️ Proceed with caution. Monitor conditions closely.")
        elif safety_level == FlightSafety.DANGEROUS:
            recommendations.append("❌ Flight not recommended. Wait for better conditions.")
        else:
            recommendations.append("🚫 DO NOT FLY. Conditions are unsafe for operations.")
        
        return recommendations
    
    def calculate_density_altitude(self, pressure_hpa: float, temperature_c: float, elevation_m: float = 0) -> float:
        """
        Calculate density altitude - critical for aircraft performance
        """
        # Convert pressure to inHg
        pressure_inhg = pressure_hpa * 0.02953
        
        # Calculate pressure altitude
        pressure_altitude = (29.92 - pressure_inhg) * 1000
        
        # Calculate density altitude
        density_altitude = pressure_altitude + (120 * (temperature_c - (15 - (pressure_altitude * 0.00198))))
        
        return density_altitude