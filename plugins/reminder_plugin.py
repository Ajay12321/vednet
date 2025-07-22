"""
Reminder Plugin for Cog AI Agent
Handles setting reminders and scheduling tasks
"""

import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from plugins.plugin_manager import BasePlugin

class ReminderPlugin(BasePlugin):
    """Plugin for setting and managing reminders"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "ReminderPlugin"
        self.version = "1.0.0"
        self.description = "Sets and manages reminders and scheduled tasks"
        self.supported_intents = ["reminder"]
        self.reminders = []
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.supported_intents
    
    async def initialize(self) -> bool:
        """Initialize the reminder plugin"""
        try:
            self.logger.info("Reminder plugin initialized")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing reminder plugin: {e}")
            return False
    
    async def execute(self, intent: str, parameters: Dict[str, Any], command: str) -> Dict[str, Any]:
        """Execute reminder setting"""
        try:
            reminder_text = parameters.get('reminder_text', 'General reminder')
            time_str = parameters.get('time', 'now')
            
            # Parse time
            reminder_time = self._parse_time(time_str)
            
            # Create reminder
            reminder = {
                "id": len(self.reminders) + 1,
                "text": reminder_text,
                "time": reminder_time,
                "created_at": datetime.now(),
                "status": "active"
            }
            
            self.reminders.append(reminder)
            
            return {
                "success": True,
                "message": f"Reminder set: '{reminder_text}' for {reminder_time.strftime('%Y-%m-%d %H:%M')}",
                "reminder": reminder,
                "task_created": True
            }
            
        except Exception as e:
            self.logger.error(f"Error setting reminder: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_time(self, time_str: str) -> datetime:
        """Parse time string to datetime"""
        now = datetime.now()
        
        if "now" in time_str.lower():
            return now
        elif "today" in time_str.lower():
            return now.replace(hour=18, minute=0, second=0)
        elif "tomorrow" in time_str.lower():
            return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0)
        elif "minutes" in time_str.lower():
            # Extract number of minutes
            import re
            match = re.search(r'(\d+)', time_str)
            if match:
                minutes = int(match.group(1))
                return now + timedelta(minutes=minutes)
        elif "hours" in time_str.lower():
            # Extract number of hours
            import re
            match = re.search(r'(\d+)', time_str)
            if match:
                hours = int(match.group(1))
                return now + timedelta(hours=hours)
        elif "pm" in time_str.lower() or "am" in time_str.lower():
            # Parse specific time
            import re
            match = re.search(r'(\d{1,2})\s*(am|pm)', time_str.lower())
            if match:
                hour = int(match.group(1))
                if match.group(2) == "pm" and hour != 12:
                    hour += 12
                elif match.group(2) == "am" and hour == 12:
                    hour = 0
                return now.replace(hour=hour, minute=0, second=0)
        
        # Default to 1 hour from now
        return now + timedelta(hours=1)
    
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Reminder plugin cleaned up")