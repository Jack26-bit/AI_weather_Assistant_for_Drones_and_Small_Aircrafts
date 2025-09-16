"""
Main application entry point for the AI Weather Assistant
"""
import sys
from datetime import datetime
from tomorrow_io_fetcher import TomorrowIOFetcher
from Weather_display import WeatherDisplay
from flight_analyzer import FlightAnalyzer
from Weather_alerts import WeatherAlerts
from config import Config

class WeatherAssistant:
    def __init__(self):
        self.weather_fetcher = TomorrowIOFetcher()
        self.display = WeatherDisplay()
        self.analyzer = FlightAnalyzer()
        self.alerts = WeatherAlerts()
        self.history = []
    
    def run(self):
        """Main application loop"""
        self.display.display_welcome_message()
        
        while True:
            try:
                command = input("\n🛩️  Enter command: ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using Weather Assistant. Fly safe!")
                    break
                elif command == 'help':
                    self.show_help()
                elif command.startswith('weather '):
                    location = command[8:].strip()
                    self.get_current_weather(location)
                elif command.startswith('forecast '):
                    location = command[9:].strip()
                    self.get_forecast(location)
                elif command == 'multi':
                    self.get_multi_location_weather()
                elif command == 'alerts':
                    self.show_active_alerts()
                elif command == 'history':
                    self.show_history()
                elif command == 'config':
                    self.show_configuration()
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    def get_current_weather(self, location: str):
        """Get and display current weather for a location"""
        if not location:
            print("❓ Please specify a location. Example: 'weather New York'")
            return
        
        print(f"🔍 Fetching weather data for {location}...")
        
        weather_data = self.weather_fetcher.get_current_weather(location)
        if weather_data:
            self.display.display_current_weather(weather_data)
            
            # Add to history
            self.history.append({
                'timestamp': datetime.now().isoformat(),
                'location': location,
                'type': 'current_weather',
                'data': weather_data
            })
            
            # Keep only last 10 entries
            if len(self.history) > 10:
                self.history.pop(0)
        else:
            print(f"❌ Could not fetch weather data for {location}")
    
    def get_forecast(self, location: str):
        """Get and display weather forecast for a location"""
        if not location:
            print("❓ Please specify a location. Example: 'forecast London'")
            return
        
        print(f"🔮 Fetching forecast for {location}...")
        
        forecast_data = self.weather_fetcher.get_forecast(location)
        if forecast_data:
            self.display.display_forecast(forecast_data, location)
        else:
            print(f"❌ Could not fetch forecast data for {location}")
    
    def get_multi_location_weather(self):
        """Get weather for multiple default locations"""
        print("🌍 Fetching weather for multiple locations...")
        
        locations = Config.DEFAULT_LOCATIONS
        weather_data = self.weather_fetcher.get_multiple_locations(locations)
        
        if weather_data:
            self.display.display_multi_location_summary(weather_data)
        else:
            print("❌ Could not fetch multi-location weather data")
    
    def show_active_alerts(self):
        """Show currently active weather alerts"""
        if self.alerts.active_alerts:
            alert_panel = self.display.console.panel(
                self.alerts.format_alerts(),
                title="🚨 Active Weather Alerts",
                border_style="red"
            )
            self.display.console.print(alert_panel)
        else:
            print("✅ No active weather alerts")
    
    def show_history(self):
        """Show recent weather query history"""
        if not self.history:
            print("📝 No weather history available")
            return
        
        print("\n📚 Recent Weather Queries:")
        print("-" * 60)
        
        for i, entry in enumerate(reversed(self.history), 1):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            location = entry['location']
            query_type = entry['type'].replace('_', ' ').title()
            
            print(f"{i:2d}. {timestamp} | {location} | {query_type}")
    
    def show_configuration(self):
        """Show current configuration settings"""
        config_info = f"""
⚙️ Configuration Settings:

Wind Speed Limits:
  • Safe: ≤ {Config.WIND_SPEED_LIMITS['safe']} km/h
  • Caution: ≤ {Config.WIND_SPEED_LIMITS['caution']} km/h  
  • Dangerous: ≤ {Config.WIND_SPEED_LIMITS['dangerous']} km/h

Visibility Limits:
  • Safe: ≥ {Config.VISIBILITY_LIMITS['safe']} km
  • Caution: ≥ {Config.VISIBILITY_LIMITS['caution']} km
  • Dangerous: ≥ {Config.VISIBILITY_LIMITS['dangerous']} km

Temperature Limits:
  • Safe Range: {Config.TEMPERATURE_LIMITS['min_safe']}°C to {Config.TEMPERATURE_LIMITS['max_safe']}°C

Default Locations: {', '.join(Config.DEFAULT_LOCATIONS)}

API Status: {'✅ Connected' if Config.OPENWEATHER_API_KEY != 'your_api_key_here' else '❌ API Key Required'}
        """
        print(config_info)
    
    def show_help(self):
        """Show help information"""
        help_text = """
🛩️ AI Weather Assistant - Available Commands:

📊 Weather Commands:
  weather <location>     - Get current weather conditions
  forecast <location>    - Get 5-day weather forecast
  multi                  - Compare weather at multiple locations
  
🚨 Safety Commands:
  alerts                 - View active weather alerts
  history               - Show recent weather queries
  config                - Show configuration settings
  
🔧 System Commands:
  help                  - Show this help message
  quit/exit/q           - Exit the application

📍 Location Examples:
  • weather New York
  • forecast London, UK
  • weather LAX (airport codes work too!)

💡 Tips:
  • Flight scores range from 0-100 (higher = safer)
  • Always check alerts before flying
  • Consider density altitude for performance planning
  • Use forecast data for flight planning
        """
        print(help_text)

def main():
    """Application entry point"""
    # Check if API key is configured
    if Config.TOMORROWIO_API_KEY == 'your_api_key_here':
        print("⚠️  WARNING: Tomorrow.io API key not configured!")
        print("Please set your API key in the .env file or environment variables.")
        print("Get a free API key at: https://tomorrow.io/")
        print("\nUsing demo mode with limited functionality...\n")
    
    # Start the application
    assistant = WeatherAssistant()
    assistant.run()

if __name__ == "__main__":
    main()