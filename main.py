#!/usr/bin/env python3
"""
VedNet - Comprehensive Task Management System
Handles daily tasks like food ordering, dress recommendations, stock predictions, and more.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
import asyncio

# Import task modules
from tasks.food_ordering import FoodOrderingManager
from tasks.dress_recommendations import DressRecommendationManager
from tasks.stock_predictions import StockPredictionManager
from tasks.weather_task import WeatherManager
from tasks.calendar_task import CalendarManager
from tasks.shopping_task import ShoppingManager
from tasks.fitness_task import FitnessManager
from tasks.finance_task import FinanceManager
from utils.config import Config
from utils.logger import setup_logger

class VedNetTaskManager:
    """Main task management system"""
    
    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.logger = setup_logger()
        
        # Initialize task managers
        self.task_managers = {
            "food": FoodOrderingManager(),
            "dress": DressRecommendationManager(),
            "stocks": StockPredictionManager(),
            "weather": WeatherManager(),
            "calendar": CalendarManager(),
            "shopping": ShoppingManager(),
            "fitness": FitnessManager(),
            "finance": FinanceManager()
        }
        
        self.completed_tasks = []
        self.pending_tasks = []
    
    def display_welcome(self):
        """Display welcome message and system info"""
        welcome_text = """
        🌟 Welcome to VedNet Task Management System 🌟
        
        Your comprehensive daily assistant for:
        • Food Ordering & Meal Planning
        • Dress & Style Recommendations  
        • Stock Market Predictions
        • Weather Updates & Planning
        • Calendar & Schedule Management
        • Shopping List & Price Tracking
        • Fitness & Health Tracking
        • Personal Finance Management
        """
        
        self.console.print(Panel(welcome_text, title="VedNet", expand=False))
    
    def display_main_menu(self):
        """Display main menu options"""
        table = Table(title="Available Tasks")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Task Category", style="magenta")
        table.add_column("Description", style="green")
        
        tasks = [
            ("1", "Food Ordering", "Order food, meal planning, restaurant recommendations"),
            ("2", "Dress & Style", "Outfit recommendations, style advice, weather-appropriate clothing"),
            ("3", "Stock Predictions", "Market analysis, stock predictions, portfolio tracking"),
            ("4", "Weather Updates", "Current weather, forecasts, alerts"),
            ("5", "Calendar Management", "Schedule appointments, reminders, time management"),
            ("6", "Shopping Assistant", "Shopping lists, price comparisons, deals"),
            ("7", "Fitness Tracking", "Workout plans, health metrics, goal tracking"),
            ("8", "Finance Management", "Budget tracking, expense analysis, financial goals"),
            ("9", "Smart Automation", "Run all daily tasks automatically"),
            ("10", "Task Status", "View completed and pending tasks"),
            ("0", "Exit", "Close the application")
        ]
        
        for task_id, category, description in tasks:
            table.add_row(task_id, category, description)
        
        self.console.print(table)
    
    async def execute_task(self, task_id: str):
        """Execute a specific task"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            
            if task_id == "1":
                task = progress.add_task("Processing food ordering...", total=None)
                result = await self.task_managers["food"].execute()
                
            elif task_id == "2":
                task = progress.add_task("Generating dress recommendations...", total=None)
                result = await self.task_managers["dress"].execute()
                
            elif task_id == "3":
                task = progress.add_task("Analyzing stock market...", total=None)
                result = await self.task_managers["stocks"].execute()
                
            elif task_id == "4":
                task = progress.add_task("Fetching weather updates...", total=None)
                result = await self.task_managers["weather"].execute()
                
            elif task_id == "5":
                task = progress.add_task("Managing calendar...", total=None)
                result = await self.task_managers["calendar"].execute()
                
            elif task_id == "6":
                task = progress.add_task("Processing shopping tasks...", total=None)
                result = await self.task_managers["shopping"].execute()
                
            elif task_id == "7":
                task = progress.add_task("Tracking fitness metrics...", total=None)
                result = await self.task_managers["fitness"].execute()
                
            elif task_id == "8":
                task = progress.add_task("Analyzing finances...", total=None)
                result = await self.task_managers["finance"].execute()
                
            elif task_id == "9":
                task = progress.add_task("Running all daily tasks...", total=None)
                result = await self.run_all_tasks()
                
            else:
                return {"status": "error", "message": "Invalid task ID"}
            
            progress.update(task, completed=True)
            
        return result
    
    async def run_all_tasks(self):
        """Run all daily tasks automatically"""
        results = {}
        
        for name, manager in self.task_managers.items():
            try:
                self.console.print(f"[blue]Executing {name} tasks...[/blue]")
                result = await manager.execute()
                results[name] = result
                
                if result.get("status") == "success":
                    self.completed_tasks.append({
                        "task": name,
                        "timestamp": datetime.now(),
                        "result": result
                    })
                else:
                    self.pending_tasks.append({
                        "task": name,
                        "timestamp": datetime.now(),
                        "error": result.get("message", "Unknown error")
                    })
                    
            except Exception as e:
                self.logger.error(f"Error executing {name}: {str(e)}")
                results[name] = {"status": "error", "message": str(e)}
        
        return {"status": "completed", "results": results}
    
    def display_task_status(self):
        """Display completed and pending tasks"""
        # Completed tasks table
        if self.completed_tasks:
            completed_table = Table(title="✅ Completed Tasks")
            completed_table.add_column("Task", style="green")
            completed_table.add_column("Completed At", style="cyan")
            completed_table.add_column("Status", style="green")
            
            for task in self.completed_tasks[-10:]:  # Show last 10
                completed_table.add_row(
                    task["task"].title(),
                    task["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    "✅ Success"
                )
            
            self.console.print(completed_table)
        
        # Pending tasks table
        if self.pending_tasks:
            pending_table = Table(title="⏳ Pending/Failed Tasks")
            pending_table.add_column("Task", style="yellow")
            pending_table.add_column("Failed At", style="cyan")
            pending_table.add_column("Error", style="red")
            
            for task in self.pending_tasks[-10:]:  # Show last 10
                pending_table.add_row(
                    task["task"].title(),
                    task["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    task["error"]
                )
            
            self.console.print(pending_table)
    
    async def main_loop(self):
        """Main application loop"""
        self.display_welcome()
        
        while True:
            try:
                self.console.print("\n" + "="*50)
                self.display_main_menu()
                
                choice = Prompt.ask(
                    "\n[bold blue]Select a task[/bold blue]",
                    choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                    default="9"
                )
                
                if choice == "0":
                    self.console.print("[bold red]Goodbye! 👋[/bold red]")
                    break
                
                elif choice == "10":
                    self.display_task_status()
                    continue
                
                # Execute the selected task
                result = await self.execute_task(choice)
                
                # Display result
                if result.get("status") == "success":
                    self.console.print(Panel(
                        f"✅ Task completed successfully!\n{result.get('message', '')}",
                        title="Success",
                        style="green"
                    ))
                else:
                    self.console.print(Panel(
                        f"❌ Task failed: {result.get('message', 'Unknown error')}",
                        title="Error",
                        style="red"
                    ))
                
                # Ask if user wants to continue
                if not Confirm.ask("\n[blue]Continue with another task?[/blue]", default=True):
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[bold red]Operation cancelled by user[/bold red]")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                self.console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")

def main():
    """Entry point"""
    try:
        # Create necessary directories
        os.makedirs("tasks", exist_ok=True)
        os.makedirs("utils", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Run the application
        app = VedNetTaskManager()
        asyncio.run(app.main_loop())
        
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Failed to start application: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()