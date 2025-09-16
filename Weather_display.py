"""
Weather display and formatting module - WebContainer compatible version
"""
from datetime import datetime
from typing import Dict, List

class WeatherDisplay:
    def __init__(self):
        # Simple color codes for terminal output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text"""
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def display_welcome_message(self):
        """Display welcome message and instructions"""
        welcome_text = f"""
{self.colorize('🛩️  AI Weather Assistant for Drones & Small Aircraft', 'bold')}
{self.colorize('=' * 60, 'blue')}

{self.colorize('Available Commands:', 'cyan')}
  • weather <location>     - Get current weather conditions
  • forecast <location>    - Get 5-day weather forecast  
  • multi                  - Compare weather at multiple locations
  • alerts                 - View active weather alerts
  • history               - Show recent weather queries
  • config                - Show configuration settings
  • help                  - Show detailed help
  • quit/exit/q           - Exit application

{self.colorize('Example:', 'yellow')} weather New York
{self.colorize('Tip:', 'green')} Flight scores range from 0-100 (higher = safer)
        """
        print(welcome_text)
    
    def display_current_weather(self, weather_data: Dict):
        """Display current weather conditions with flight analysis"""
        from flight_analyzer import FlightAnalyzer
        analyzer = FlightAnalyzer()
        
        # Calculate flight score
        flight_score = analyzer.calculate_flight_score(weather_data)
        safety_level = analyzer.get_safety_level(flight_score)
        
        # Choose color based on safety level
        score_color = {
            'SAFE': 'green',
            'CAUTION': 'yellow', 
            'DANGEROUS': 'red'
        }.get(safety_level, 'white')
        
        print(f"\n{self.colorize('📍 Current Weather Report', 'bold')}")
        print(f"{self.colorize('=' * 50, 'blue')}")
        print(f"Location: {self.colorize(weather_data['location'], 'cyan')}")
        print(f"Time: {datetime.fromisoformat(weather_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n{self.colorize('🌤️  Weather Conditions:', 'bold')}")
        print(f"  Condition: {weather_data['weather']['description'].title()}")
        print(f"  Temperature: {weather_data['temperature']['current']:.1f}°C (feels like {weather_data['temperature']['feels_like']:.1f}°C)")
        print(f"  Humidity: {weather_data['temperature']['humidity']}%")
        print(f"  Pressure: {weather_data['pressure']} hPa")
        print(f"  Cloudiness: {weather_data['cloudiness']}%")
        
        print(f"\n{self.colorize('💨 Wind Analysis:', 'bold')}")
        print(f"  Speed: {weather_data['wind']['speed']:.1f} km/h")
        print(f"  Direction: {weather_data['wind']['direction']}°")
        if weather_data['wind']['gust'] > 0:
            print(f"  Gusts: {weather_data['wind']['gust']:.1f} km/h")
        
        print(f"\n{self.colorize('👁️  Visibility & Precipitation:', 'bold')}")
        print(f"  Visibility: {weather_data['visibility']:.1f} km")
        if weather_data['precipitation']['rain_1h'] > 0:
            print(f"  Rain (1h): {weather_data['precipitation']['rain_1h']} mm")
        if weather_data['precipitation']['snow_1h'] > 0:
            print(f"  Snow (1h): {weather_data['precipitation']['snow_1h']} mm")
        
        print(f"\n{self.colorize('🌅 Sun Times:', 'bold')}")
        print(f"  Sunrise: {weather_data['sunrise']}")
        print(f"  Sunset: {weather_data['sunset']}")
        
        print(f"\n{self.colorize('✈️  Flight Safety Analysis:', 'bold')}")
        print(f"  Flight Score: {self.colorize(f'{flight_score}/100', score_color)}")
        print(f"  Safety Level: {self.colorize(safety_level, score_color)}")
        
        # Display recommendations
        recommendations = analyzer.get_flight_recommendations(weather_data)
        if recommendations:
            print(f"\n{self.colorize('💡 Recommendations:', 'bold')}")
            for rec in recommendations:
                print(f"  • {rec}")
    
    def display_forecast(self, forecast_data: List[Dict], location: str):
        """Display weather forecast"""
        print(f"\n{self.colorize(f'🔮 5-Day Forecast for {location}', 'bold')}")
        print(f"{self.colorize('=' * 60, 'blue')}")
        
        # Group by day
        daily_forecasts = {}
        for item in forecast_data:
            date = datetime.fromisoformat(item['datetime']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        for date, day_data in list(daily_forecasts.items())[:5]:
            print(f"\n{self.colorize(date.strftime('%A, %B %d'), 'cyan')}")
            print("-" * 30)
            
            # Show morning, afternoon, evening forecasts
            times_of_day = ['Morning', 'Afternoon', 'Evening']
            for i, period in enumerate(times_of_day):
                if i * 3 < len(day_data):
                    item = day_data[i * 3]
                    time_str = datetime.fromisoformat(item['datetime']).strftime('%H:%M')
                    print(f"  {period} ({time_str}):")
                    print(f"    Temp: {item['temperature']:.1f}°C")
                    print(f"    Weather: {item['weather'].title()}")
                    print(f"    Wind: {item['wind_speed']:.1f} km/h")
                    print(f"    Humidity: {item['humidity']}%")
    
    def display_multi_location_summary(self, weather_data: Dict[str, Dict]):
        """Display weather summary for multiple locations"""
        print(f"\n{self.colorize('🌍 Multi-Location Weather Summary', 'bold')}")
        print(f"{self.colorize('=' * 70, 'blue')}")
        
        from flight_analyzer import FlightAnalyzer
        analyzer = FlightAnalyzer()
        
        for location, data in weather_data.items():
            flight_score = analyzer.calculate_flight_score(data)
            safety_level = analyzer.get_safety_level(flight_score)
            
            score_color = {
                'SAFE': 'green',
                'CAUTION': 'yellow',
                'DANGEROUS': 'red'
            }.get(safety_level, 'white')
            
            print(f"\n📍 {self.colorize(data['location'], 'cyan')}")
            print(f"   Weather: {data['weather']['description'].title()}")
            print(f"   Temp: {data['temperature']['current']:.1f}°C | Wind: {data['wind']['speed']:.1f} km/h")
            print(f"   Visibility: {data['visibility']:.1f} km | Humidity: {data['temperature']['humidity']}%")
            print(f"   Flight Score: {self.colorize(f'{flight_score}/100 ({safety_level})', score_color)}")