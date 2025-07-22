"""
Weather Updates and Planning Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests
from utils.config import Config
from utils.logger import setup_logger

class WeatherManager:
    """Manages weather updates and planning"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("weather")
        self.api_key = self.config.get("api_keys.openweather")
        self.location = self.config.get("user_preferences.location", "New York, NY")
    
    async def get_current_weather(self):
        """Get current weather conditions"""
        if self.api_key:
            try:
                # OpenWeatherMap API call
                url = f"http://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.api_key}&units=metric"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "location": data["name"],
                        "temperature": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "description": data["weather"][0]["description"].title(),
                        "wind_speed": data["wind"]["speed"],
                        "visibility": data.get("visibility", "N/A"),
                        "uv_index": "N/A"  # Would need separate UV API call
                    }
            except Exception as e:
                self.logger.warning(f"Error fetching real weather data: {e}")
        
        # Fallback to mock data
        return self._generate_mock_weather()
    
    def _generate_mock_weather(self):
        """Generate mock weather data"""
        conditions = [
            {"temp": 22, "desc": "Sunny", "humidity": 45, "wind": 8},
            {"temp": 15, "desc": "Partly Cloudy", "humidity": 60, "wind": 12},
            {"temp": 8, "desc": "Rainy", "humidity": 85, "wind": 15},
            {"temp": -2, "desc": "Snow", "humidity": 90, "wind": 20},
            {"temp": 28, "desc": "Clear", "humidity": 40, "wind": 5}
        ]
        
        weather = random.choice(conditions)
        
        return {
            "location": self.location,
            "temperature": weather["temp"],
            "feels_like": weather["temp"] - 2,
            "humidity": weather["humidity"],
            "pressure": random.randint(1010, 1025),
            "description": weather["desc"],
            "wind_speed": weather["wind"],
            "visibility": random.randint(8, 15),
            "uv_index": random.randint(1, 10)
        }
    
    async def get_forecast(self, days: int = 5):
        """Get weather forecast"""
        if self.api_key:
            try:
                # OpenWeatherMap forecast API
                url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.location}&appid={self.api_key}&units=metric"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    forecast = []
                    
                    # Process 5-day forecast (3-hour intervals)
                    for i in range(0, min(len(data["list"]), days * 8), 8):  # Every 24 hours
                        item = data["list"][i]
                        date = datetime.fromtimestamp(item["dt"])
                        
                        forecast.append({
                            "date": date.strftime("%Y-%m-%d"),
                            "day": date.strftime("%A"),
                            "high_temp": round(item["main"]["temp_max"]),
                            "low_temp": round(item["main"]["temp_min"]),
                            "description": item["weather"][0]["description"].title(),
                            "humidity": item["main"]["humidity"],
                            "wind_speed": item["wind"]["speed"],
                            "precipitation": item.get("rain", {}).get("3h", 0)
                        })
                    
                    return forecast
            except Exception as e:
                self.logger.warning(f"Error fetching real forecast data: {e}")
        
        # Fallback to mock data
        return self._generate_mock_forecast(days)
    
    def _generate_mock_forecast(self, days: int):
        """Generate mock forecast data"""
        forecast = []
        base_temp = 20
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            temp_variation = random.randint(-5, 5)
            
            conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Clear"]
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "high_temp": base_temp + temp_variation + random.randint(3, 8),
                "low_temp": base_temp + temp_variation - random.randint(3, 8),
                "description": random.choice(conditions),
                "humidity": random.randint(40, 80),
                "wind_speed": random.randint(5, 20),
                "precipitation": random.randint(0, 30) if random.random() > 0.7 else 0
            })
        
        return forecast
    
    async def get_weather_alerts(self):
        """Get weather alerts and warnings"""
        # In a real implementation, this would fetch from weather API
        current_weather = await self.get_current_weather()
        alerts = []
        
        # Generate alerts based on conditions
        if current_weather["temperature"] > 35:
            alerts.append({
                "type": "Heat Warning",
                "severity": "High",
                "message": "Extreme heat expected. Stay hydrated and avoid prolonged sun exposure."
            })
        elif current_weather["temperature"] < -10:
            alerts.append({
                "type": "Cold Warning",
                "severity": "High",
                "message": "Extreme cold conditions. Dress warmly and limit outdoor exposure."
            })
        
        if current_weather["wind_speed"] > 25:
            alerts.append({
                "type": "Wind Advisory",
                "severity": "Medium",
                "message": "Strong winds expected. Secure loose objects."
            })
        
        if "rain" in current_weather["description"].lower():
            alerts.append({
                "type": "Rain Advisory",
                "severity": "Low",
                "message": "Rain expected. Carry an umbrella and drive carefully."
            })
        
        return alerts
    
    async def get_outfit_suggestions(self):
        """Get outfit suggestions based on weather"""
        current_weather = await self.get_current_weather()
        temp = current_weather["temperature"]
        condition = current_weather["description"].lower()
        
        suggestions = {
            "temperature_advice": "",
            "clothing_suggestions": [],
            "accessories": []
        }
        
        # Temperature-based suggestions
        if temp > 25:
            suggestions["temperature_advice"] = "Hot weather - dress light and breathable"
            suggestions["clothing_suggestions"] = ["Light t-shirt", "Shorts", "Sandals", "Sun hat"]
            suggestions["accessories"] = ["Sunglasses", "Sunscreen", "Water bottle"]
        elif temp > 15:
            suggestions["temperature_advice"] = "Mild weather - comfortable layers"
            suggestions["clothing_suggestions"] = ["Light sweater", "Jeans", "Sneakers"]
            suggestions["accessories"] = ["Light jacket", "Sunglasses"]
        elif temp > 0:
            suggestions["temperature_advice"] = "Cool weather - warm layers needed"
            suggestions["clothing_suggestions"] = ["Warm sweater", "Long pants", "Closed shoes", "Jacket"]
            suggestions["accessories"] = ["Scarf", "Light gloves"]
        else:
            suggestions["temperature_advice"] = "Cold weather - bundle up warmly"
            suggestions["clothing_suggestions"] = ["Heavy coat", "Thermal layers", "Warm boots", "Thick sweater"]
            suggestions["accessories"] = ["Warm hat", "Gloves", "Scarf", "Warm socks"]
        
        # Condition-based adjustments
        if "rain" in condition:
            suggestions["accessories"].extend(["Umbrella", "Waterproof jacket"])
        if "snow" in condition:
            suggestions["accessories"].extend(["Waterproof boots", "Extra warm layers"])
        if "wind" in condition:
            suggestions["accessories"].append("Windproof jacket")
        
        return suggestions
    
    async def plan_outdoor_activities(self):
        """Suggest outdoor activities based on weather"""
        current_weather = await self.get_current_weather()
        forecast = await self.get_forecast(3)
        
        activities = []
        
        # Current day activities
        temp = current_weather["temperature"]
        condition = current_weather["description"].lower()
        
        if "sunny" in condition or "clear" in condition:
            if 20 <= temp <= 30:
                activities.append({
                    "activity": "Perfect for outdoor picnic or hiking",
                    "time": "Today",
                    "suitability": "Excellent"
                })
            elif temp > 30:
                activities.append({
                    "activity": "Swimming or water activities",
                    "time": "Today",
                    "suitability": "Good (stay hydrated)"
                })
        
        elif "cloudy" in condition:
            activities.append({
                "activity": "Great for walking or light outdoor sports",
                "time": "Today",
                "suitability": "Good"
            })
        
        elif "rain" in condition:
            activities.append({
                "activity": "Indoor activities recommended",
                "time": "Today",
                "suitability": "Poor for outdoor"
            })
        
        # Future days planning
        for day in forecast:
            if "sunny" in day["description"].lower() and 18 <= day["high_temp"] <= 28:
                activities.append({
                    "activity": f"Excellent day for outdoor activities on {day['day']}",
                    "time": day["date"],
                    "suitability": "Excellent"
                })
        
        return activities
    
    async def execute(self):
        """Execute weather tasks"""
        try:
            self.logger.info("Starting weather tasks...")
            
            # Get current weather
            current_weather = await self.get_current_weather()
            
            # Get forecast
            forecast = await self.get_forecast(5)
            
            # Get weather alerts
            alerts = await self.get_weather_alerts()
            
            # Get outfit suggestions
            outfit_suggestions = await self.get_outfit_suggestions()
            
            # Plan outdoor activities
            activities = await self.plan_outdoor_activities()
            
            result = {
                "status": "success",
                "message": "Weather tasks completed successfully!",
                "data": {
                    "current_weather": {
                        "location": current_weather["location"],
                        "temperature": current_weather["temperature"],
                        "description": current_weather["description"],
                        "humidity": current_weather["humidity"]
                    },
                    "forecast_summary": f"{len(forecast)} day forecast available",
                    "alerts_count": len(alerts),
                    "outfit_advice": outfit_suggestions["temperature_advice"],
                    "activities_suggested": len(activities)
                }
            }
            
            # Save detailed weather data
            weather_file = f"data/weather_{datetime.now().strftime('%Y%m%d')}.json"
            detailed_data = {
                "current_weather": current_weather,
                "forecast": forecast,
                "alerts": alerts,
                "outfit_suggestions": outfit_suggestions,
                "activities": activities,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(weather_file, 'w') as f:
                json.dump(detailed_data, f, indent=2)
            
            self.logger.info("Weather tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in weather tasks: {str(e)}")
            return {"status": "error", "message": f"Weather tasks failed: {str(e)}"}