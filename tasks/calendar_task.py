"""
Calendar Management and Schedule Planning Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.config import Config
from utils.logger import setup_logger

class CalendarManager:
    """Manages calendar events and schedule planning"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("calendar")
        self.events = self._load_events()
        self.recurring_events = self._load_recurring_events()
    
    def _load_events(self):
        """Load existing calendar events"""
        try:
            with open("data/calendar_events.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _load_recurring_events(self):
        """Load recurring events templates"""
        return [
            {"title": "Team Meeting", "day": "Monday", "time": "09:00", "duration": 60},
            {"title": "Gym Workout", "day": "Tuesday", "time": "18:00", "duration": 90},
            {"title": "Doctor Checkup", "day": "Monthly", "time": "14:00", "duration": 30},
            {"title": "Weekly Review", "day": "Friday", "time": "16:00", "duration": 30}
        ]
    
    async def add_event(self, title: str, date: str, time: str, duration: int = 60, description: str = ""):
        """Add a new calendar event"""
        event = {
            "id": f"evt_{random.randint(1000, 9999)}",
            "title": title,
            "date": date,
            "time": time,
            "duration": duration,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "reminder_set": True
        }
        
        self.events.append(event)
        await self._save_events()
        
        return event
    
    async def _save_events(self):
        """Save events to file"""
        with open("data/calendar_events.json", 'w') as f:
            json.dump(self.events, f, indent=2)
    
    async def get_today_schedule(self):
        """Get today's schedule"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_events = [event for event in self.events if event["date"] == today]
        
        # Add recurring events for today
        weekday = datetime.now().strftime("%A")
        for recurring in self.recurring_events:
            if recurring["day"] == weekday:
                today_events.append({
                    "title": recurring["title"],
                    "time": recurring["time"],
                    "duration": recurring["duration"],
                    "type": "recurring"
                })
        
        # Sort by time
        today_events.sort(key=lambda x: x["time"])
        
        return today_events
    
    async def get_week_schedule(self):
        """Get this week's schedule"""
        week_schedule = {}
        
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            weekday = date.strftime("%A")
            
            day_events = [event for event in self.events if event["date"] == date_str]
            
            # Add recurring events
            for recurring in self.recurring_events:
                if recurring["day"] == weekday:
                    day_events.append({
                        "title": recurring["title"],
                        "time": recurring["time"],
                        "duration": recurring["duration"],
                        "type": "recurring"
                    })
            
            week_schedule[weekday] = {
                "date": date_str,
                "events": sorted(day_events, key=lambda x: x["time"])
            }
        
        return week_schedule
    
    async def find_free_time(self, duration: int = 60, date: str = None):
        """Find available time slots"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Get events for the day
        day_events = [event for event in self.events if event["date"] == date]
        
        # Working hours (9 AM to 6 PM)
        working_start = 9 * 60  # 9:00 AM in minutes
        working_end = 18 * 60   # 6:00 PM in minutes
        
        # Convert events to time blocks
        busy_blocks = []
        for event in day_events:
            time_parts = event["time"].split(":")
            start_minutes = int(time_parts[0]) * 60 + int(time_parts[1])
            end_minutes = start_minutes + event["duration"]
            busy_blocks.append((start_minutes, end_minutes))
        
        # Sort busy blocks
        busy_blocks.sort()
        
        # Find free slots
        free_slots = []
        current_time = working_start
        
        for start, end in busy_blocks:
            if current_time + duration <= start:
                slot_start_hour = current_time // 60
                slot_start_min = current_time % 60
                free_slots.append(f"{slot_start_hour:02d}:{slot_start_min:02d}")
            current_time = max(current_time, end)
        
        # Check for time after last meeting
        if current_time + duration <= working_end:
            slot_start_hour = current_time // 60
            slot_start_min = current_time % 60
            free_slots.append(f"{slot_start_hour:02d}:{slot_start_min:02d}")
        
        return free_slots
    
    async def suggest_meeting_times(self, duration: int = 60, days_ahead: int = 7):
        """Suggest optimal meeting times"""
        suggestions = []
        
        for i in range(1, days_ahead + 1):
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            free_slots = await self.find_free_time(duration, date)
            
            if free_slots:
                suggestions.append({
                    "date": date,
                    "day": (datetime.now() + timedelta(days=i)).strftime("%A"),
                    "available_times": free_slots[:3]  # Top 3 suggestions
                })
        
        return suggestions
    
    async def set_reminders(self):
        """Set reminders for upcoming events"""
        reminders = []
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Tomorrow's events
        tomorrow_events = [event for event in self.events if event["date"] == tomorrow]
        
        for event in tomorrow_events:
            reminders.append({
                "type": "event_reminder",
                "message": f"Reminder: {event['title']} tomorrow at {event['time']}",
                "event_id": event.get("id"),
                "time": event["time"]
            })
        
        # Weekly prep reminder
        if datetime.now().weekday() == 6:  # Sunday
            reminders.append({
                "type": "weekly_prep",
                "message": "Time to plan your week ahead!",
                "action": "review_schedule"
            })
        
        return reminders
    
    async def analyze_schedule_patterns(self):
        """Analyze schedule patterns and productivity"""
        if not self.events:
            return {"message": "No events to analyze"}
        
        # Count meetings by day of week
        weekday_counts = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
        
        for event in self.events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            weekday = event_date.strftime("%A")
            if weekday in weekday_counts:
                weekday_counts[weekday] += 1
        
        # Find busiest day
        busiest_day = max(weekday_counts, key=weekday_counts.get)
        
        # Calculate average meeting duration
        total_duration = sum(event.get("duration", 60) for event in self.events)
        avg_duration = total_duration / len(self.events) if self.events else 0
        
        return {
            "total_events": len(self.events),
            "busiest_day": busiest_day,
            "average_meeting_duration": round(avg_duration, 1),
            "weekday_distribution": weekday_counts,
            "suggestions": [
                "Consider batch meetings on specific days",
                "Block time for focused work",
                "Review meeting necessity and duration"
            ]
        }
    
    async def create_time_blocks(self):
        """Create time blocks for different activities"""
        time_blocks = [
            {"name": "Deep Work", "start": "09:00", "end": "11:00", "type": "focus"},
            {"name": "Communication", "start": "11:00", "end": "12:00", "type": "admin"},
            {"name": "Lunch Break", "start": "12:00", "end": "13:00", "type": "break"},
            {"name": "Meetings", "start": "13:00", "end": "15:00", "type": "collaboration"},
            {"name": "Project Work", "start": "15:00", "end": "17:00", "type": "execution"},
            {"name": "Planning", "start": "17:00", "end": "18:00", "type": "planning"}
        ]
        
        return time_blocks
    
    async def execute(self):
        """Execute calendar management tasks"""
        try:
            self.logger.info("Starting calendar management tasks...")
            
            # Get today's schedule
            today_schedule = await self.get_today_schedule()
            
            # Get week overview
            week_schedule = await self.get_week_schedule()
            
            # Find free time today
            free_time = await self.find_free_time(60)
            
            # Get meeting suggestions
            meeting_suggestions = await self.suggest_meeting_times(60, 5)
            
            # Set reminders
            reminders = await self.set_reminders()
            
            # Analyze patterns
            schedule_analysis = await self.analyze_schedule_patterns()
            
            # Create time blocks
            time_blocks = await self.create_time_blocks()
            
            result = {
                "status": "success",
                "message": "Calendar management tasks completed successfully!",
                "data": {
                    "today_events_count": len(today_schedule),
                    "free_time_slots": len(free_time),
                    "reminders_set": len(reminders),
                    "meeting_suggestions": len(meeting_suggestions),
                    "schedule_analysis": {
                        "total_events": schedule_analysis.get("total_events", 0),
                        "busiest_day": schedule_analysis.get("busiest_day", "N/A")
                    }
                }
            }
            
            # Save detailed calendar data
            calendar_file = f"data/calendar_summary_{datetime.now().strftime('%Y%m%d')}.json"
            detailed_data = {
                "today_schedule": today_schedule,
                "week_schedule": week_schedule,
                "free_time": free_time,
                "meeting_suggestions": meeting_suggestions,
                "reminders": reminders,
                "schedule_analysis": schedule_analysis,
                "time_blocks": time_blocks,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(calendar_file, 'w') as f:
                json.dump(detailed_data, f, indent=2)
            
            self.logger.info("Calendar management tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in calendar management tasks: {str(e)}")
            return {"status": "error", "message": f"Calendar management failed: {str(e)}"}