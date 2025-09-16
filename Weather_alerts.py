"""
Weather alert system for critical conditions
"""
from typing import Dict, List
from datetime import datetime
from enum import Enum

class AlertLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"

class WeatherAlert:
    def __init__(self, level: AlertLevel, title: str, message: str, timestamp: str = None):
        self.level = level
        self.title = title
        self.message = message
        self.timestamp = timestamp or datetime.now().isoformat()

class WeatherAlerts:
    def __init__(self):
        self.active_alerts = []
    
    def check_weather_alerts(self, weather_data: Dict) -> List[WeatherAlert]:
        """
        Check weather data for alert conditions
        """
        alerts = []
        
        # Wind alerts
        wind_speed = weather_data['wind']['speed']
        if wind_speed > 40:
            alerts.append(WeatherAlert(
                AlertLevel.EMERGENCY,
                "Extreme Wind Warning",
                f"Wind speed {wind_speed:.1f} km/h exceeds safe limits. DO NOT FLY."
            ))
        elif wind_speed > 30:
            alerts.append(WeatherAlert(
                AlertLevel.CRITICAL,
                "High Wind Warning",
                f"Wind speed {wind_speed:.1f} km/h. Flight operations not recommended."
            ))
        elif wind_speed > 20:
            alerts.append(WeatherAlert(
                AlertLevel.WARNING,
                "Wind Advisory",
                f"Wind speed {wind_speed:.1f} km/h. Exercise extreme caution."
            ))
        
        # Visibility alerts
        visibility = weather_data['visibility']
        if visibility < 1:
            alerts.append(WeatherAlert(
                AlertLevel.CRITICAL,
                "Low Visibility Warning",
                f"Visibility {visibility:.1f} km. Visual flight rules not recommended."
            ))
        elif visibility < 3:
            alerts.append(WeatherAlert(
                AlertLevel.WARNING,
                "Reduced Visibility",
                f"Visibility {visibility:.1f} km. Maintain visual observers."
            ))
        
        # Temperature alerts
        temp = weather_data['temperature']['current']
        if temp < -15:
            alerts.append(WeatherAlert(
                AlertLevel.CRITICAL,
                "Extreme Cold Warning",
                f"Temperature {temp:.1f}°C. Battery and equipment failure risk."
            ))
        elif temp > 45:
            alerts.append(WeatherAlert(
                AlertLevel.CRITICAL,
                "Extreme Heat Warning",
                f"Temperature {temp:.1f}°C. Overheating risk for electronics."
            ))
        
        # Precipitation alerts
        rain = weather_data['precipitation']['rain_1h']
        snow = weather_data['precipitation']['snow_1h']
        
        if rain > 10 or snow > 10:
            alerts.append(WeatherAlert(
                AlertLevel.CRITICAL,
                "Heavy Precipitation Warning",
                "Heavy rain/snow detected. Equipment damage risk."
            ))
        elif rain > 2.5 or snow > 2.5:
            alerts.append(WeatherAlert(
                AlertLevel.WARNING,
                "Precipitation Advisory",
                "Moderate precipitation. Protect equipment from moisture."
            ))
        
        # Pressure alerts (rapid changes)
        pressure = weather_data['pressure']
        if pressure < 980:
            alerts.append(WeatherAlert(
                AlertLevel.WARNING,
                "Low Pressure System",
                f"Low barometric pressure {pressure} hPa. Storm system possible."
            ))
        elif pressure > 1030:
            alerts.append(WeatherAlert(
                AlertLevel.INFO,
                "High Pressure System",
                f"High barometric pressure {pressure} hPa. Stable conditions expected."
            ))
        
        # Weather condition alerts
        weather_main = weather_data['weather']['main'].lower()
        if 'thunderstorm' in weather_main:
            alerts.append(WeatherAlert(
                AlertLevel.EMERGENCY,
                "Thunderstorm Warning",
                "Thunderstorm conditions detected. IMMEDIATE LANDING REQUIRED."
            ))
        elif 'tornado' in weather_main:
            alerts.append(WeatherAlert(
                AlertLevel.EMERGENCY,
                "Tornado Warning",
                "Tornado activity detected. SEEK IMMEDIATE SHELTER."
            ))
        
        self.active_alerts = alerts
        return alerts
    
    def get_alert_summary(self) -> str:
        """
        Get a summary of active alerts
        """
        if not self.active_alerts:
            return "✅ No active weather alerts"
        
        alert_counts = {}
        for alert in self.active_alerts:
            level = alert.level.value
            alert_counts[level] = alert_counts.get(level, 0) + 1
        
        summary_parts = []
        for level, count in alert_counts.items():
            emoji = {
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'CRITICAL': '🚨',
                'EMERGENCY': '🆘'
            }.get(level, '📢')
            
            summary_parts.append(f"{emoji} {count} {level}")
        
        return f"Active Alerts: {', '.join(summary_parts)}"
    
    def format_alerts(self) -> str:
        """
        Format alerts for display
        """
        if not self.active_alerts:
            return "✅ No weather alerts"
        
        formatted = []
        for alert in self.active_alerts:
            emoji = {
                AlertLevel.INFO: 'ℹ️',
                AlertLevel.WARNING: '⚠️',
                AlertLevel.CRITICAL: '🚨',
                AlertLevel.EMERGENCY: '🆘'
            }.get(alert.level, '📢')
            
            formatted.append(f"{emoji} {alert.level.value}: {alert.title}")
            formatted.append(f"   {alert.message}")
        
        return '\n'.join(formatted)