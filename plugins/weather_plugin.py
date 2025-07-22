"""
Weather Plugin for Cog AI Agent
Handles weather information queries
"""

import asyncio
from typing import Dict, List, Any
from plugins.plugin_manager import BasePlugin

class WeatherPlugin(BasePlugin):
    """Plugin for weather information"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "WeatherPlugin"
        self.version = "1.0.0"
        self.description = "Provides weather information"
        self.supported_intents = ["weather"]
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.supported_intents
    
    async def execute(self, intent: str, parameters: Dict[str, Any], command: str) -> Dict[str, Any]:
        """Get weather information"""
        location = parameters.get('location', 'current location')
        
        # Mock weather data
        weather_data = {
            "location": location,
            "temperature": "24°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "10 km/h",
            "visibility": "8 km"
        }
        
        return {
            "success": True,
            "response": f"Weather in {location}: {weather_data['temperature']}, {weather_data['condition']}",
            "weather_data": weather_data
        }