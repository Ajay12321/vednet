"""
Configuration Management for Cog AI Agent
"""

import os
import json
import logging
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for Cog AI Agent"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables"""
        # Default configuration
        self._config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'voice_enabled': True,
            'wake_word': 'Hey Cog',
            'voice_rate': 180,
            'voice_volume': 0.8,
            'max_concurrent_tasks': 5,
            'task_timeout': 300,
            'database_path': 'cog_agent.db',
            'log_level': 'INFO',
            'platforms': {
                'swiggy': {'enabled': True},
                'zomato': {'enabled': True},
                'amazon': {'enabled': True},
                'flipkart': {'enabled': True},
                'bookmyshow': {'enabled': True}
            }
        }
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                self._config.update(file_config)
                self.logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                self.logger.error(f"Error loading config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self._config[key] = value
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving config file: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()