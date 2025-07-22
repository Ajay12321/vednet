"""
Fitness Tracking and Health Management Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.config import Config
from utils.logger import setup_logger

class FitnessManager:
    """Manages fitness tracking and health goals"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("fitness")
        self.fitness_data = self._load_fitness_data()
        self.workout_library = self._load_workout_library()
        self.goals = self._load_fitness_goals()
    
    def _load_fitness_data(self):
        """Load existing fitness data"""
        try:
            with open("data/fitness_data.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"workouts": [], "daily_metrics": [], "achievements": []}
    
    def _load_workout_library(self):
        """Load workout templates"""
        return {
            "cardio": [
                {"name": "Morning Run", "duration": 30, "calories": 300, "intensity": "medium"},
                {"name": "HIIT Training", "duration": 20, "calories": 250, "intensity": "high"},
                {"name": "Cycling", "duration": 45, "calories": 400, "intensity": "medium"},
                {"name": "Swimming", "duration": 30, "calories": 350, "intensity": "medium"}
            ],
            "strength": [
                {"name": "Full Body Workout", "duration": 60, "calories": 200, "intensity": "high"},
                {"name": "Upper Body", "duration": 45, "calories": 150, "intensity": "medium"},
                {"name": "Lower Body", "duration": 45, "calories": 180, "intensity": "medium"},
                {"name": "Core Training", "duration": 30, "calories": 120, "intensity": "medium"}
            ],
            "flexibility": [
                {"name": "Yoga Session", "duration": 60, "calories": 150, "intensity": "low"},
                {"name": "Stretching", "duration": 15, "calories": 30, "intensity": "low"},
                {"name": "Pilates", "duration": 45, "calories": 180, "intensity": "medium"}
            ]
        }
    
    def _load_fitness_goals(self):
        """Load fitness goals from config"""
        return self.config.get("user_preferences.fitness_goals", {
            "daily_steps": 10000,
            "weekly_workouts": 3,
            "weekly_calories": 1500,
            "target_weight": 70,
            "water_intake": 8  # glasses per day
        })
    
    async def log_workout(self, workout_type: str, duration: int, intensity: str = "medium"):
        """Log a completed workout"""
        # Calculate calories burned (simplified)
        intensity_multiplier = {"low": 0.8, "medium": 1.0, "high": 1.3}
        base_calories = duration * 5  # 5 calories per minute base
        calories_burned = int(base_calories * intensity_multiplier.get(intensity, 1.0))
        
        workout = {
            "id": f"workout_{random.randint(1000, 9999)}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "type": workout_type,
            "duration": duration,
            "intensity": intensity,
            "calories_burned": calories_burned,
            "logged_at": datetime.now().isoformat()
        }
        
        self.fitness_data["workouts"].append(workout)
        await self._save_fitness_data()
        
        return workout
    
    async def log_daily_metrics(self, steps: int = None, weight: float = None, water_glasses: int = None):
        """Log daily health metrics"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if metrics for today already exist
        existing_metric = None
        for metric in self.fitness_data["daily_metrics"]:
            if metric["date"] == today:
                existing_metric = metric
                break
        
        if existing_metric:
            # Update existing metrics
            if steps is not None:
                existing_metric["steps"] = steps
            if weight is not None:
                existing_metric["weight"] = weight
            if water_glasses is not None:
                existing_metric["water_glasses"] = water_glasses
            existing_metric["updated_at"] = datetime.now().isoformat()
        else:
            # Create new daily metrics
            daily_metric = {
                "date": today,
                "steps": steps or random.randint(6000, 12000),
                "weight": weight or round(random.uniform(65, 75), 1),
                "water_glasses": water_glasses or random.randint(6, 10),
                "logged_at": datetime.now().isoformat()
            }
            self.fitness_data["daily_metrics"].append(daily_metric)
        
        await self._save_fitness_data()
        return existing_metric or daily_metric
    
    async def _save_fitness_data(self):
        """Save fitness data to file"""
        with open("data/fitness_data.json", 'w') as f:
            json.dump(self.fitness_data, f, indent=2)
    
    async def get_workout_recommendations(self):
        """Get personalized workout recommendations"""
        recommendations = []
        
        # Analyze recent workout history
        recent_workouts = [w for w in self.fitness_data["workouts"] 
                          if datetime.now() - datetime.fromisoformat(w["logged_at"]) <= timedelta(days=7)]
        
        workout_types = [w["type"] for w in recent_workouts]
        
        # Recommend based on balance
        if workout_types.count("cardio") < 2:
            cardio_workout = random.choice(self.workout_library["cardio"])
            recommendations.append({
                "type": "cardio",
                "workout": cardio_workout,
                "reason": "Need more cardiovascular exercise this week"
            })
        
        if workout_types.count("strength") < 2:
            strength_workout = random.choice(self.workout_library["strength"])
            recommendations.append({
                "type": "strength",
                "workout": strength_workout,
                "reason": "Add strength training for balanced fitness"
            })
        
        if not any("flexibility" in wt for wt in workout_types):
            flexibility_workout = random.choice(self.workout_library["flexibility"])
            recommendations.append({
                "type": "flexibility",
                "workout": flexibility_workout,
                "reason": "Include flexibility work for recovery"
            })
        
        return recommendations[:3]  # Top 3 recommendations
    
    async def track_goals_progress(self):
        """Track progress toward fitness goals"""
        today = datetime.now().strftime("%Y-%m-%d")
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        
        # Daily goals progress
        today_metrics = None
        for metric in self.fitness_data["daily_metrics"]:
            if metric["date"] == today:
                today_metrics = metric
                break
        
        daily_progress = {}
        if today_metrics:
            daily_progress = {
                "steps": {
                    "current": today_metrics["steps"],
                    "goal": self.goals["daily_steps"],
                    "percentage": min(100, (today_metrics["steps"] / self.goals["daily_steps"]) * 100)
                },
                "water": {
                    "current": today_metrics["water_glasses"],
                    "goal": self.goals["water_intake"],
                    "percentage": min(100, (today_metrics["water_glasses"] / self.goals["water_intake"]) * 100)
                }
            }
        
        # Weekly goals progress
        week_workouts = [w for w in self.fitness_data["workouts"]
                        if w["date"] >= week_start]
        
        week_calories = sum(w["calories_burned"] for w in week_workouts)
        
        weekly_progress = {
            "workouts": {
                "current": len(week_workouts),
                "goal": self.goals["weekly_workouts"],
                "percentage": min(100, (len(week_workouts) / self.goals["weekly_workouts"]) * 100)
            },
            "calories": {
                "current": week_calories,
                "goal": self.goals["weekly_calories"],
                "percentage": min(100, (week_calories / self.goals["weekly_calories"]) * 100)
            }
        }
        
        return {
            "daily_progress": daily_progress,
            "weekly_progress": weekly_progress
        }
    
    async def analyze_fitness_trends(self):
        """Analyze fitness trends and patterns"""
        if not self.fitness_data["workouts"]:
            return {"message": "No workout data to analyze"}
        
        # Workout frequency analysis
        workout_days = {}
        for workout in self.fitness_data["workouts"]:
            date = datetime.fromisoformat(workout["logged_at"])
            day = date.strftime("%A")
            workout_days[day] = workout_days.get(day, 0) + 1
        
        most_active_day = max(workout_days, key=workout_days.get) if workout_days else "N/A"
        
        # Average calories per workout
        total_calories = sum(w["calories_burned"] for w in self.fitness_data["workouts"])
        avg_calories = total_calories / len(self.fitness_data["workouts"])
        
        # Workout type distribution
        type_distribution = {}
        for workout in self.fitness_data["workouts"]:
            workout_type = workout["type"]
            type_distribution[workout_type] = type_distribution.get(workout_type, 0) + 1
        
        return {
            "total_workouts": len(self.fitness_data["workouts"]),
            "most_active_day": most_active_day,
            "average_calories_per_workout": round(avg_calories, 1),
            "workout_type_distribution": type_distribution,
            "suggestions": [
                "Try to maintain consistency in workout schedule",
                "Mix different types of workouts for balance",
                "Track recovery days to prevent overtraining"
            ]
        }
    
    async def create_weekly_plan(self):
        """Create a balanced weekly workout plan"""
        plan = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Basic weekly template
        weekly_template = [
            {"day": "Monday", "type": "strength", "focus": "Upper Body"},
            {"day": "Tuesday", "type": "cardio", "focus": "HIIT"},
            {"day": "Wednesday", "type": "flexibility", "focus": "Yoga"},
            {"day": "Thursday", "type": "strength", "focus": "Lower Body"},
            {"day": "Friday", "type": "cardio", "focus": "Endurance"},
            {"day": "Saturday", "type": "strength", "focus": "Full Body"},
            {"day": "Sunday", "type": "flexibility", "focus": "Recovery"}
        ]
        
        for template in weekly_template:
            day = template["day"]
            workout_type = template["type"]
            
            if workout_type in self.workout_library:
                workout = random.choice(self.workout_library[workout_type])
                plan[day] = {
                    "workout": workout,
                    "focus": template["focus"],
                    "recommended_time": "Morning" if day in ["Monday", "Wednesday", "Friday"] else "Evening"
                }
        
        return plan
    
    async def get_nutrition_suggestions(self):
        """Get basic nutrition suggestions based on activity"""
        recent_workouts = [w for w in self.fitness_data["workouts"] 
                          if datetime.now() - datetime.fromisoformat(w["logged_at"]) <= timedelta(days=1)]
        
        suggestions = []
        
        if recent_workouts:
            total_calories_burned = sum(w["calories_burned"] for w in recent_workouts)
            
            if total_calories_burned > 300:
                suggestions.extend([
                    "Increase protein intake for muscle recovery",
                    "Stay hydrated - aim for extra 2-3 glasses of water",
                    "Include complex carbohydrates for energy replenishment"
                ])
            else:
                suggestions.extend([
                    "Maintain balanced nutrition with lean proteins",
                    "Include plenty of vegetables and fruits",
                    "Stay adequately hydrated throughout the day"
                ])
        else:
            suggestions.extend([
                "Focus on nutrient-dense foods",
                "Prepare for tomorrow's workout with good nutrition",
                "Consider light, healthy snacks between meals"
            ])
        
        return suggestions
    
    async def check_achievements(self):
        """Check for new fitness achievements"""
        achievements = []
        
        # Steps achievements
        today_metrics = None
        for metric in self.fitness_data["daily_metrics"]:
            if metric["date"] == datetime.now().strftime("%Y-%m-%d"):
                today_metrics = metric
                break
        
        if today_metrics and today_metrics["steps"] >= self.goals["daily_steps"]:
            achievements.append({
                "type": "daily_steps",
                "title": "Daily Steps Goal Achieved!",
                "description": f"Reached {today_metrics['steps']} steps today"
            })
        
        # Workout streak
        consecutive_days = 0
        current_date = datetime.now().date()
        
        for i in range(7):  # Check last 7 days
            check_date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            day_workouts = [w for w in self.fitness_data["workouts"] if w["date"] == check_date]
            
            if day_workouts:
                consecutive_days += 1
            else:
                break
        
        if consecutive_days >= 3:
            achievements.append({
                "type": "workout_streak",
                "title": f"{consecutive_days}-Day Workout Streak!",
                "description": "Keep up the consistency!"
            })
        
        return achievements
    
    async def execute(self):
        """Execute fitness tracking tasks"""
        try:
            self.logger.info("Starting fitness tracking tasks...")
            
            # Log today's simulated metrics if not already logged
            await self.log_daily_metrics()
            
            # Get workout recommendations
            workout_recommendations = await self.get_workout_recommendations()
            
            # Track goals progress
            goals_progress = await self.track_goals_progress()
            
            # Analyze fitness trends
            fitness_trends = await self.analyze_fitness_trends()
            
            # Create weekly plan
            weekly_plan = await self.create_weekly_plan()
            
            # Get nutrition suggestions
            nutrition_suggestions = await self.get_nutrition_suggestions()
            
            # Check achievements
            achievements = await self.check_achievements()
            
            result = {
                "status": "success",
                "message": "Fitness tracking tasks completed successfully!",
                "data": {
                    "workout_recommendations": len(workout_recommendations),
                    "daily_goals_progress": goals_progress.get("daily_progress", {}),
                    "weekly_goals_progress": goals_progress.get("weekly_progress", {}),
                    "total_workouts": fitness_trends.get("total_workouts", 0),
                    "achievements_earned": len(achievements)
                }
            }
            
            # Save detailed fitness data
            fitness_file = f"data/fitness_summary_{datetime.now().strftime('%Y%m%d')}.json"
            detailed_data = {
                "workout_recommendations": workout_recommendations,
                "goals_progress": goals_progress,
                "fitness_trends": fitness_trends,
                "weekly_plan": weekly_plan,
                "nutrition_suggestions": nutrition_suggestions,
                "achievements": achievements,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(fitness_file, 'w') as f:
                json.dump(detailed_data, f, indent=2)
            
            self.logger.info("Fitness tracking tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in fitness tracking tasks: {str(e)}")
            return {"status": "error", "message": f"Fitness tracking failed: {str(e)}"}