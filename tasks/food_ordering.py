"""
Food Ordering and Meal Planning Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests
from utils.config import Config
from utils.logger import setup_logger

class FoodOrderingManager:
    """Manages food ordering, restaurant recommendations, and meal planning"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("food_ordering")
        self.restaurants_db = self._load_restaurants_db()
        self.meal_plans = self._load_meal_plans()
    
    def _load_restaurants_db(self):
        """Load restaurant database"""
        return {
            "italian": [
                {"name": "Luigi's Pizza", "rating": 4.5, "price": 25, "delivery_time": 30},
                {"name": "Mama Mia's", "rating": 4.8, "price": 35, "delivery_time": 45},
                {"name": "Romano's Bistro", "rating": 4.2, "price": 40, "delivery_time": 35}
            ],
            "indian": [
                {"name": "Spice Garden", "rating": 4.6, "price": 22, "delivery_time": 25},
                {"name": "Curry House", "rating": 4.4, "price": 28, "delivery_time": 40},
                {"name": "Tandoor Express", "rating": 4.7, "price": 30, "delivery_time": 35}
            ],
            "mexican": [
                {"name": "El Sombrero", "rating": 4.3, "price": 18, "delivery_time": 20},
                {"name": "Taco Fiesta", "rating": 4.5, "price": 24, "delivery_time": 30},
                {"name": "Burrito Palace", "rating": 4.1, "price": 20, "delivery_time": 25}
            ],
            "chinese": [
                {"name": "Golden Dragon", "rating": 4.4, "price": 26, "delivery_time": 35},
                {"name": "Panda Express", "rating": 4.2, "price": 15, "delivery_time": 20},
                {"name": "Szechuan Palace", "rating": 4.7, "price": 32, "delivery_time": 40}
            ],
            "american": [
                {"name": "Burger Junction", "rating": 4.3, "price": 16, "delivery_time": 25},
                {"name": "BBQ Master", "rating": 4.6, "price": 28, "delivery_time": 35},
                {"name": "Diner Classic", "rating": 4.1, "price": 22, "delivery_time": 30}
            ]
        }
    
    def _load_meal_plans(self):
        """Load meal planning templates"""
        return {
            "healthy": {
                "breakfast": ["Oatmeal with fruits", "Greek yogurt with granola", "Smoothie bowl"],
                "lunch": ["Grilled chicken salad", "Quinoa bowl", "Vegetable soup"],
                "dinner": ["Baked salmon with vegetables", "Lean beef stir-fry", "Vegetarian pasta"]
            },
            "budget": {
                "breakfast": ["Scrambled eggs", "Toast with peanut butter", "Cereal"],
                "lunch": ["Sandwich", "Instant noodles", "Rice and beans"],
                "dinner": ["Pasta with marinara", "Fried rice", "Bean burrito"]
            },
            "quick": {
                "breakfast": ["Granola bar", "Instant oatmeal", "Banana"],
                "lunch": ["Salad kit", "Microwave meal", "Sandwich"],
                "dinner": ["Takeout", "Frozen pizza", "Fast food"]
            }
        }
    
    async def get_restaurant_recommendations(self, preferences: Dict = None):
        """Get restaurant recommendations based on preferences"""
        if not preferences:
            preferences = self.config.get("user_preferences", {})
        
        cuisine_prefs = preferences.get("cuisine_preferences", ["italian"])
        budget_range = preferences.get("budget_range", {"min": 10, "max": 50})
        
        recommendations = []
        
        for cuisine in cuisine_prefs:
            if cuisine.lower() in self.restaurants_db:
                restaurants = self.restaurants_db[cuisine.lower()]
                
                # Filter by budget
                filtered = [
                    r for r in restaurants 
                    if budget_range["min"] <= r["price"] <= budget_range["max"]
                ]
                
                # Sort by rating
                filtered.sort(key=lambda x: x["rating"], reverse=True)
                recommendations.extend(filtered[:2])  # Top 2 per cuisine
        
        return recommendations
    
    async def create_meal_plan(self, days: int = 7, plan_type: str = "healthy"):
        """Create a meal plan for specified days"""
        if plan_type not in self.meal_plans:
            plan_type = "healthy"
        
        meal_plan = {}
        template = self.meal_plans[plan_type]
        
        for day in range(days):
            date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
            
            meal_plan[date] = {
                "breakfast": random.choice(template["breakfast"]),
                "lunch": random.choice(template["lunch"]),
                "dinner": random.choice(template["dinner"])
            }
        
        # Save meal plan
        meal_plan_file = f"data/meal_plan_{datetime.now().strftime('%Y%m%d')}.json"
        with open(meal_plan_file, 'w') as f:
            json.dump(meal_plan, f, indent=2)
        
        return meal_plan
    
    async def order_food(self, restaurant: str, items: List[str]):
        """Simulate food ordering"""
        # In a real implementation, this would integrate with delivery APIs
        order_id = f"ORD{random.randint(1000, 9999)}"
        estimated_delivery = datetime.now() + timedelta(minutes=random.randint(20, 60))
        
        order_details = {
            "order_id": order_id,
            "restaurant": restaurant,
            "items": items,
            "status": "confirmed",
            "estimated_delivery": estimated_delivery.strftime("%H:%M"),
            "total_price": random.randint(15, 45)
        }
        
        # Save order
        orders_file = "data/food_orders.json"
        orders = []
        try:
            with open(orders_file, 'r') as f:
                orders = json.load(f)
        except FileNotFoundError:
            pass
        
        orders.append(order_details)
        with open(orders_file, 'w') as f:
            json.dump(orders, f, indent=2)
        
        return order_details
    
    async def get_nutrition_info(self, food_item: str):
        """Get basic nutrition information"""
        # Simplified nutrition database
        nutrition_db = {
            "pizza": {"calories": 285, "protein": 12, "carbs": 36, "fat": 10},
            "burger": {"calories": 540, "protein": 25, "carbs": 40, "fat": 31},
            "salad": {"calories": 150, "protein": 8, "carbs": 12, "fat": 6},
            "pasta": {"calories": 220, "protein": 8, "carbs": 44, "fat": 1},
            "sushi": {"calories": 200, "protein": 18, "carbs": 20, "fat": 6}
        }
        
        # Find closest match
        for item, info in nutrition_db.items():
            if item.lower() in food_item.lower():
                return info
        
        # Default values if not found
        return {"calories": 300, "protein": 15, "carbs": 30, "fat": 12}
    
    async def execute(self):
        """Execute food ordering tasks"""
        try:
            self.logger.info("Starting food ordering tasks...")
            
            # Get restaurant recommendations
            recommendations = await self.get_restaurant_recommendations()
            
            # Create weekly meal plan
            meal_plan = await self.create_meal_plan(7, "healthy")
            
            # Suggest today's meal based on meal plan
            today = datetime.now().strftime("%Y-%m-%d")
            today_meals = meal_plan.get(today, {})
            
            # Get nutrition info for today's dinner
            dinner_nutrition = await self.get_nutrition_info(today_meals.get("dinner", ""))
            
            result = {
                "status": "success",
                "message": f"Food tasks completed successfully!",
                "data": {
                    "restaurant_recommendations": recommendations[:3],
                    "today_meal_plan": today_meals,
                    "dinner_nutrition": dinner_nutrition,
                    "weekly_meal_plan_created": True
                }
            }
            
            self.logger.info("Food ordering tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in food ordering tasks: {str(e)}")
            return {"status": "error", "message": f"Food ordering failed: {str(e)}"}
    
    async def quick_order(self):
        """Quick order based on preferences"""
        recommendations = await self.get_restaurant_recommendations()
        if recommendations:
            restaurant = recommendations[0]
            # Simulate ordering popular items
            popular_items = ["Special of the day", "Chef's recommendation", "Popular combo"]
            order = await self.order_food(restaurant["name"], popular_items[:2])
            return order
        
        return None