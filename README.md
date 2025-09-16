# AI_weather_Assistant_for_Drones_and_Small_Aircrafts
A comprehensive weather analysis system designed specifically for drone operators and small aircraft pilots. This assistant provides real-time weather monitoring, flight safety analysis, and intelligent recommendations to ensure safe flight operations.
## Features

### 🌤️ Weather Monitoring
- Real-time weather data from OpenWeatherMap API
- Detailed weather conditions including temperature, humidity, pressure
- Wind analysis with speed, direction, and gust information
- Visibility and precipitation monitoring
- Cloud cover analysis

### ✈️ Flight Safety Analysis
- Intelligent flight safety scoring (0-100 scale)
- Multi-factor analysis considering wind, visibility, temperature, and precipitation
- Density altitude calculations for performance planning
- Customizable safety thresholds for different aircraft types

### 🚨 Weather Alerts System
- Automatic detection of dangerous weather conditions
- Multi-level alert system (Info, Warning, Critical, Emergency)
- Real-time monitoring for thunderstorms, high winds, and low visibility
- Custom alert thresholds

### 📊 Data Visualization
- Rich console interface with color-coded displays
- Formatted weather tables and panels
- Multi-location weather comparison
- Historical weather query tracking

### 🔮 Forecasting
- 5-day weather forecast with hourly breakdowns
- Future flight condition predictions
- Trend analysis for flight planning

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd weather-assistant
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
   - Copy `.env.example` to `.env`
   - Add your API key to the `.env` file:
     ```
     OPENWEATHER_API_KEY=your_actual_api_key_here
     ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

### Basic Commands

- `weather <location>` - Get current weather conditions
- `forecast <location>` - Get 5-day weather forecast  
- `multi` - Compare weather at multiple locations
- `alerts` - View active weather alerts
- `history` - Show recent weather queries
- `help` - Show all available commands
- `quit` - Exit the application

### Example Usage

```bash
🛩️  Enter command: weather New York
🛩️  Enter command: forecast London, UK  
🛩️  Enter command: multi
🛩️  Enter command: alerts
```

## Flight Safety Scoring

The system calculates a comprehensive flight safety score (0-100) based on:

- **Wind Conditions (30%)** - Speed, gusts, and direction
- **Visibility (25%)** - Current visibility distance
- **Temperature (15%)** - Battery performance and equipment safety
- **Precipitation (20%)** - Rain and snow conditions
- **Cloud Cover (10%)** - Overall sky conditions

### Safety Levels

- **SAFE (80-100)** ✅ - Ideal conditions for flight
- **CAUTION (60-79)** ⚠️ - Proceed with extra care
- **DANGEROUS (30-59)** ❌ - Flight not recommended
- **NO FLY (0-29)** 🚫 - Unsafe conditions

## Configuration

Customize safety thresholds in `config.py`:

```python
WIND_SPEED_LIMITS = {
    'safe': 10,      # km/h
    'caution': 20,   # km/h
    'dangerous': 30  # km/h
}

VISIBILITY_LIMITS = {
    'safe': 10,      # km
    'caution': 3,    # km
    'dangerous': 1   # km
}

TEMPERATURE_LIMITS = {
    'min_safe': -10,  # °C
    'max_safe': 40,   # °C
}
```

## Weather Alerts

The system automatically monitors for:

- **Wind Alerts** - High wind speeds and gusts
- **Visibility Alerts** - Low visibility conditions
- **Temperature Alerts** - Extreme hot/cold conditions
- **Precipitation Alerts** - Rain and snow warnings
- **Pressure Alerts** - Rapid pressure changes
- **Severe Weather** - Thunderstorms, tornadoes

## Technical Details

### Architecture

- **weather_fetcher.py** - API integration and data retrieval
- **flight_analyzer.py** - Safety scoring and analysis algorithms
- **weather_alerts.py** - Alert detection and management
- **weather_display.py** - User interface and data presentation
- **main.py** - Application entry point and command handling
- **config.py** - Configuration and settings management

### Dependencies

- `requests` - HTTP API calls
- `python-dotenv` - Environment variable management
- `rich` - Enhanced console output
- `tabulate` - Data table formatting
- `geopy` - Location processing
- `matplotlib` - Data visualization (future use)
- `numpy` - Numerical calculations

## Safety Considerations

⚠️ **IMPORTANT SAFETY NOTICE**

This tool is designed to assist with flight planning and weather analysis, but should not be the sole source for flight safety decisions. Always:

- Verify weather conditions with multiple sources
- Follow local aviation regulations and guidelines
- Consider your aircraft's specific limitations
- Use proper pre-flight inspection procedures
- Maintain visual observers when required
- Have emergency procedures in place

## API Limits

The free OpenWeatherMap API includes:
- 60 calls per minute
- 1,000 calls per day
- Current weather and 5-day forecast access

For higher usage, consider upgrading to a paid plan.

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional weather data sources
- Machine learning for improved predictions
- Mobile app integration
- Flight log integration
- Advanced visualization features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on the project repository.

---

**Stay informed, stay safe, and happy flying!** ✈️🌤️
