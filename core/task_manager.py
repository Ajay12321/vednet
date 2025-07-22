"""
Task Manager Module for Cog AI Agent
Handles task scheduling, execution, and management
"""

import asyncio
import logging
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import schedule
from dataclasses import dataclass, asdict

@dataclass
class Task:
    """Task data structure"""
    id: str
    type: str
    status: str  # pending, running, completed, failed
    created_at: datetime
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    command: str = ""
    parameters: Dict[str, Any] = None
    result: Dict[str, Any] = None
    priority: int = 5  # 1-10, 1 is highest priority
    max_retries: int = 3
    retry_count: int = 0
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.result is None:
            self.result = {}

class TaskManager:
    """
    Manages task execution, scheduling, and tracking
    """
    
    def __init__(self, config, database):
        self.config = config
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # Task storage
        self.tasks: Dict[str, Task] = {}
        self.scheduled_tasks: List[Task] = []
        self.active_tasks: List[Task] = []
        
        # Task execution settings
        self.max_concurrent_tasks = 5
        self.task_timeout = 300  # 5 minutes
        
        self.logger.info("Task Manager initialized")
    
    async def create_task(
        self,
        task_type: str,
        command: str,
        parameters: Dict[str, Any] = None,
        scheduled_at: datetime = None,
        priority: int = 5
    ) -> str:
        """
        Create a new task
        
        Args:
            task_type: Type of task
            command: Original command
            parameters: Task parameters
            scheduled_at: When to execute (None for immediate)
            priority: Task priority (1-10)
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            type=task_type,
            status="pending",
            created_at=datetime.now(),
            scheduled_at=scheduled_at,
            command=command,
            parameters=parameters or {},
            priority=priority
        )
        
        self.tasks[task_id] = task
        
        if scheduled_at and scheduled_at > datetime.now():
            self.scheduled_tasks.append(task)
            self.logger.info(f"Task {task_id} scheduled for {scheduled_at}")
        else:
            # Execute immediately
            await self._execute_task(task)
        
        # Save to database
        self.database.save_task(task)
        
        return task_id
    
    async def _execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        self.logger.info(f"Executing task {task.id}: {task.type}")
        
        task.status = "running"
        self.active_tasks.append(task)
        
        try:
            # Execute based on task type
            if task.type == "food_order":
                result = await self._execute_food_order(task)
            elif task.type == "movie_booking":
                result = await self._execute_movie_booking(task)
            elif task.type == "shopping":
                result = await self._execute_shopping(task)
            elif task.type == "reminder":
                result = await self._execute_reminder(task)
            elif task.type == "weather":
                result = await self._execute_weather(task)
            elif task.type == "news":
                result = await self._execute_news(task)
            elif task.type == "search":
                result = await self._execute_search(task)
            else:
                result = {"error": f"Unknown task type: {task.type}"}
            
            task.result = result
            task.status = "completed" if not result.get('error') else "failed"
            task.completed_at = datetime.now()
            
            self.logger.info(f"Task {task.id} completed with status: {task.status}")
            
        except Exception as e:
            self.logger.error(f"Error executing task {task.id}: {e}")
            task.result = {"error": str(e)}
            task.status = "failed"
            task.completed_at = datetime.now()
            
            # Retry if possible
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "pending"
                task.completed_at = None
                self.logger.info(f"Retrying task {task.id} (attempt {task.retry_count + 1})")
                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
                return await self._execute_task(task)
        
        finally:
            if task in self.active_tasks:
                self.active_tasks.remove(task)
            
            # Update database
            self.database.update_task(task)
        
        return task.result
    
    async def _execute_food_order(self, task: Task) -> Dict[str, Any]:
        """Execute food ordering task"""
        parameters = task.parameters
        
        # Simulate food ordering process
        platform = parameters.get('platform', 'swiggy')
        food_type = parameters.get('food_type', 'pizza')
        quantity = parameters.get('quantity', 1)
        
        self.logger.info(f"Ordering {quantity} {food_type} from {platform}")
        
        # Here you would integrate with actual food delivery APIs
        # For now, we'll simulate the process
        await asyncio.sleep(2)  # Simulate processing time
        
        return {
            "success": True,
            "message": f"Order placed for {quantity} {food_type} from {platform}",
            "order_id": f"ORDER_{uuid.uuid4().hex[:8].upper()}",
            "estimated_delivery": "30-45 minutes",
            "total_cost": f"₹{quantity * 299}"
        }
    
    async def _execute_movie_booking(self, task: Task) -> Dict[str, Any]:
        """Execute movie booking task"""
        parameters = task.parameters
        
        movie_name = parameters.get('movie_name', 'Latest Movie')
        time = parameters.get('time', 'evening')
        
        self.logger.info(f"Booking ticket for {movie_name} at {time}")
        
        # Simulate booking process
        await asyncio.sleep(2)
        
        return {
            "success": True,
            "message": f"Movie ticket booked for {movie_name}",
            "booking_id": f"BMS_{uuid.uuid4().hex[:8].upper()}",
            "movie": movie_name,
            "time": time,
            "theater": "PVR Cinemas",
            "seats": "F12, F13",
            "total_cost": "₹400"
        }
    
    async def _execute_shopping(self, task: Task) -> Dict[str, Any]:
        """Execute shopping task"""
        parameters = task.parameters
        
        item_type = parameters.get('item_type', 'item')
        color = parameters.get('color', '')
        platform = parameters.get('platform', 'amazon')
        
        item_description = f"{color} {item_type}".strip()
        
        self.logger.info(f"Searching for {item_description} on {platform}")
        
        # Simulate shopping process
        await asyncio.sleep(2)
        
        return {
            "success": True,
            "message": f"Found {item_description} on {platform}",
            "item": item_description,
            "platform": platform,
            "price": "₹1,299",
            "availability": "In Stock",
            "delivery": "Tomorrow"
        }
    
    async def _execute_reminder(self, task: Task) -> Dict[str, Any]:
        """Execute reminder task"""
        parameters = task.parameters
        
        reminder_text = parameters.get('reminder_text', 'General reminder')
        time = parameters.get('time', 'now')
        
        self.logger.info(f"Setting reminder: {reminder_text} at {time}")
        
        # For now, just log the reminder
        # In a full implementation, this would integrate with calendar/notification systems
        
        return {
            "success": True,
            "message": f"Reminder set: {reminder_text}",
            "reminder": reminder_text,
            "time": time
        }
    
    async def _execute_weather(self, task: Task) -> Dict[str, Any]:
        """Execute weather query task"""
        parameters = task.parameters
        location = parameters.get('location', 'current location')
        
        self.logger.info(f"Getting weather for {location}")
        
        # Simulate weather API call
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "location": location,
            "temperature": "24°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind": "10 km/h"
        }
    
    async def _execute_news(self, task: Task) -> Dict[str, Any]:
        """Execute news query task"""
        parameters = task.parameters
        category = parameters.get('category', 'general')
        
        self.logger.info(f"Getting {category} news")
        
        # Simulate news API call
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "category": category,
            "headlines": [
                "Tech stocks rise amid AI optimism",
                "New breakthrough in renewable energy",
                "Global climate summit concludes"
            ]
        }
    
    async def _execute_search(self, task: Task) -> Dict[str, Any]:
        """Execute search task"""
        parameters = task.parameters
        query = parameters.get('query', task.command)
        
        self.logger.info(f"Searching for: {query}")
        
        # Simulate search
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "query": query,
            "results": [
                {"title": f"Result 1 for {query}", "url": "https://example.com/1"},
                {"title": f"Result 2 for {query}", "url": "https://example.com/2"},
                {"title": f"Result 3 for {query}", "url": "https://example.com/3"}
            ]
        }
    
    async def check_scheduled_tasks(self):
        """Check and execute scheduled tasks"""
        current_time = datetime.now()
        
        for task in self.scheduled_tasks[:]:  # Copy list to avoid modification issues
            if task.scheduled_at and task.scheduled_at <= current_time:
                self.scheduled_tasks.remove(task)
                await self._execute_task(task)
    
    async def process_pending_tasks(self):
        """Process pending tasks"""
        pending_tasks = [t for t in self.tasks.values() if t.status == "pending"]
        
        # Sort by priority and creation time
        pending_tasks.sort(key=lambda t: (t.priority, t.created_at))
        
        # Execute tasks up to concurrent limit
        while len(self.active_tasks) < self.max_concurrent_tasks and pending_tasks:
            task = pending_tasks.pop(0)
            if task.scheduled_at is None or task.scheduled_at <= datetime.now():
                asyncio.create_task(self._execute_task(task))
    
    async def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get list of active tasks"""
        return [asdict(task) for task in self.active_tasks]
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        task = self.tasks.get(task_id)
        return asdict(task) if task else None
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        task = self.tasks.get(task_id)
        if task and task.status in ["pending", "scheduled"]:
            task.status = "cancelled"
            if task in self.scheduled_tasks:
                self.scheduled_tasks.remove(task)
            self.database.update_task(task)
            self.logger.info(f"Task {task_id} cancelled")
            return True
        return False
    
    async def get_task_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get task history"""
        tasks = list(self.tasks.values())
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return [asdict(task) for task in tasks[:limit]]
    
    async def save_pending_tasks(self):
        """Save pending tasks to database"""
        for task in self.tasks.values():
            if task.status in ["pending", "scheduled"]:
                self.database.save_task(task)
        self.logger.info("Pending tasks saved")
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get task execution statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
        failed_tasks = len([t for t in self.tasks.values() if t.status == "failed"])
        pending_tasks = len([t for t in self.tasks.values() if t.status == "pending"])
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "pending_tasks": pending_tasks,
            "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "active_tasks": len(self.active_tasks)
        }