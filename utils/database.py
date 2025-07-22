"""
Database Management for Cog AI Agent
"""

import sqlite3
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from core.task_manager import Task

class Database:
    """Database manager for Cog AI Agent"""
    
    def __init__(self, db_path: str = "cog_agent.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.connection = None
    
    def initialize(self):
        """Initialize database and create tables"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            self.logger.info("Database initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                scheduled_at TIMESTAMP,
                completed_at TIMESTAMP,
                command TEXT,
                parameters TEXT,
                result TEXT,
                priority INTEGER DEFAULT 5,
                retry_count INTEGER DEFAULT 0
            )
        """)
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Command history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                intent TEXT,
                parameters TEXT,
                response TEXT,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
    
    def save_task(self, task: Task):
        """Save task to database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tasks 
                (id, type, status, created_at, scheduled_at, completed_at, 
                 command, parameters, result, priority, retry_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                task.type,
                task.status,
                task.created_at,
                task.scheduled_at,
                task.completed_at,
                task.command,
                json.dumps(task.parameters),
                json.dumps(task.result),
                task.priority,
                task.retry_count
            ))
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error saving task: {e}")
    
    def update_task(self, task: Task):
        """Update task in database"""
        self.save_task(task)  # Same as save for SQLite
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            self.logger.error(f"Error getting task: {e}")
            return None
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get tasks by status"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting tasks by status: {e}")
            return []
    
    def log_task(self, task_type: str, command: str, parameters: Dict[str, Any], status: str):
        """Log a task execution"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO command_history (command, intent, parameters, success)
                VALUES (?, ?, ?, ?)
            """, (command, task_type, json.dumps(parameters), status == "completed"))
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error logging task: {e}")
    
    def log_command(self, command: str, intent: str, parameters: Dict[str, Any], 
                   response: str, success: bool):
        """Log a command execution"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO command_history (command, intent, parameters, response, success)
                VALUES (?, ?, ?, ?, ?)
            """, (command, intent, json.dumps(parameters), response, success))
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error logging command: {e}")
    
    def get_command_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get command history"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM command_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting command history: {e}")
            return []
    
    def save_preference(self, key: str, value: Any):
        """Save user preference"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_preferences (key, value)
                VALUES (?, ?)
            """, (key, json.dumps(value)))
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error saving preference: {e}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return default
        except Exception as e:
            self.logger.error(f"Error getting preference: {e}")
            return default
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")