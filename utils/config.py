"""
Configuration management for VedNet Task Management System
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Configuration manager"""
    
    def __init__(self):
        load_dotenv()
        self.config_file = "data/config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file and environment"""
        # Default configuration
        self.config = {
            "api_keys": {
                "openweather": os.getenv("OPENWEATHER_API_KEY", ""),
                "food_delivery": os.getenv("FOOD_DELIVERY_API_KEY", ""),
                "openai": os.getenv("OPENAI_API_KEY", ""),
                "alpha_vantage": os.getenv("ALPHA_VANTAGE_API_KEY", "")
            },
            "user_preferences": {
                "location": "New York, NY",
                "cuisine_preferences": ["Italian", "Indian", "Mexican"],
                "dietary_restrictions": [],
                "budget_range": {"min": 10, "max": 50},
                "style_preferences": ["casual", "business", "formal"],
                "fitness_goals": {"daily_steps": 10000, "weekly_workouts": 3}
            },
            "notifications": {
                "email_enabled": False,
                "push_enabled": True,
                "reminder_times": ["09:00", "13:00", "18:00"]
            }
        }
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()