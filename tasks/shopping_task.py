"""
Shopping Assistant and Price Tracking Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.config import Config
from utils.logger import setup_logger

class ShoppingManager:
    """Manages shopping lists and price tracking"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("shopping")
        self.shopping_lists = self._load_shopping_lists()
        self.price_database = self._load_price_database()
        self.stores = self._load_stores()
    
    def _load_shopping_lists(self):
        """Load existing shopping lists"""
        try:
            with open("data/shopping_lists.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"grocery": [], "household": [], "electronics": [], "clothing": []}
    
    def _load_price_database(self):
        """Load price database for comparison"""
        return {
            # Grocery items
            "milk": {"walmart": 3.50, "target": 3.75, "whole_foods": 4.25},
            "bread": {"walmart": 2.25, "target": 2.50, "whole_foods": 3.50},
            "eggs": {"walmart": 2.75, "target": 3.00, "whole_foods": 4.50},
            "bananas": {"walmart": 1.25, "target": 1.50, "whole_foods": 2.00},
            "chicken_breast": {"walmart": 8.50, "target": 9.00, "whole_foods": 12.00},
            
            # Electronics
            "bluetooth_headphones": {"amazon": 89.99, "best_buy": 99.99, "target": 94.99},
            "laptop_charger": {"amazon": 45.99, "best_buy": 59.99, "apple_store": 79.00},
            "phone_case": {"amazon": 15.99, "target": 19.99, "carrier_store": 29.99},
            
            # Household
            "detergent": {"walmart": 8.99, "target": 9.49, "amazon": 10.99},
            "toilet_paper": {"walmart": 12.99, "costco": 18.99, "target": 14.99},
            "cleaning_spray": {"walmart": 3.99, "target": 4.49, "home_depot": 5.99}
        }
    
    def _load_stores(self):
        """Load store information"""
        return {
            "walmart": {"type": "grocery", "distance": 2.5, "rating": 4.0},
            "target": {"type": "general", "distance": 3.2, "rating": 4.2},
            "whole_foods": {"type": "grocery", "distance": 4.1, "rating": 4.5},
            "amazon": {"type": "online", "distance": 0, "rating": 4.3},
            "best_buy": {"type": "electronics", "distance": 5.8, "rating": 4.1},
            "costco": {"type": "wholesale", "distance": 6.2, "rating": 4.4}
        }
    
    async def add_to_list(self, category: str, item: str, quantity: int = 1, priority: str = "medium"):
        """Add item to shopping list"""
        if category not in self.shopping_lists:
            self.shopping_lists[category] = []
        
        new_item = {
            "name": item,
            "quantity": quantity,
            "priority": priority,
            "added_date": datetime.now().isoformat(),
            "estimated_price": self._estimate_price(item),
            "purchased": False
        }
        
        self.shopping_lists[category].append(new_item)
        await self._save_shopping_lists()
        
        return new_item
    
    def _estimate_price(self, item: str):
        """Estimate price for an item"""
        item_lower = item.lower().replace(" ", "_")
        
        if item_lower in self.price_database:
            prices = list(self.price_database[item_lower].values())
            return round(sum(prices) / len(prices), 2)
        
        # Category-based estimation
        if any(keyword in item_lower for keyword in ["milk", "bread", "egg", "fruit", "vegetable"]):
            return round(random.uniform(2.0, 8.0), 2)
        elif any(keyword in item_lower for keyword in ["electronic", "tech", "phone", "computer"]):
            return round(random.uniform(20.0, 200.0), 2)
        elif any(keyword in item_lower for keyword in ["clean", "detergent", "soap", "paper"]):
            return round(random.uniform(3.0, 15.0), 2)
        else:
            return round(random.uniform(5.0, 25.0), 2)
    
    async def _save_shopping_lists(self):
        """Save shopping lists to file"""
        with open("data/shopping_lists.json", 'w') as f:
            json.dump(self.shopping_lists, f, indent=2)
    
    async def get_price_comparison(self, item: str):
        """Get price comparison across stores"""
        item_lower = item.lower().replace(" ", "_")
        
        if item_lower in self.price_database:
            prices = self.price_database[item_lower]
            
            # Sort by price
            sorted_prices = sorted(prices.items(), key=lambda x: x[1])
            
            return {
                "item": item,
                "best_price": {
                    "store": sorted_prices[0][0],
                    "price": sorted_prices[0][1]
                },
                "all_prices": prices,
                "savings": round(sorted_prices[-1][1] - sorted_prices[0][1], 2)
            }
        
        return {"item": item, "message": "Price data not available"}
    
    async def optimize_shopping_route(self, category: str = None):
        """Optimize shopping route based on stores and items"""
        items_to_buy = []
        
        if category:
            items_to_buy = [item for item in self.shopping_lists.get(category, []) if not item["purchased"]]
        else:
            for cat_items in self.shopping_lists.values():
                items_to_buy.extend([item for item in cat_items if not item["purchased"]])
        
        if not items_to_buy:
            return {"message": "No items to purchase"}
        
        # Group items by best store
        store_groups = {}
        total_savings = 0
        
        for item in items_to_buy:
            comparison = await self.get_price_comparison(item["name"])
            if "best_price" in comparison:
                store = comparison["best_price"]["store"]
                price = comparison["best_price"]["price"]
                
                if store not in store_groups:
                    store_groups[store] = {"items": [], "total_cost": 0}
                
                store_groups[store]["items"].append({
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": price,
                    "total": price * item["quantity"]
                })
                store_groups[store]["total_cost"] += price * item["quantity"]
                total_savings += comparison.get("savings", 0)
        
        # Calculate route efficiency
        route_plan = []
        for store, data in store_groups.items():
            store_info = self.stores.get(store, {})
            route_plan.append({
                "store": store,
                "distance": store_info.get("distance", 0),
                "items_count": len(data["items"]),
                "total_cost": round(data["total_cost"], 2),
                "rating": store_info.get("rating", 0)
            })
        
        # Sort by efficiency (items per distance)
        route_plan.sort(key=lambda x: x["items_count"] / max(x["distance"], 0.1), reverse=True)
        
        return {
            "total_items": len(items_to_buy),
            "stores_to_visit": len(route_plan),
            "estimated_savings": round(total_savings, 2),
            "route_plan": route_plan,
            "store_groups": store_groups
        }
    
    async def get_deals_and_coupons(self):
        """Get current deals and coupons"""
        # Simulate deals and coupons
        deals = [
            {"store": "walmart", "item": "groceries", "discount": "20% off $50+", "expires": "2024-01-15"},
            {"store": "target", "item": "electronics", "discount": "$10 off $100+", "expires": "2024-01-20"},
            {"store": "whole_foods", "item": "organic_produce", "discount": "Buy 2 Get 1 Free", "expires": "2024-01-12"},
            {"store": "amazon", "item": "prime_members", "discount": "Free shipping + 5% back", "expires": "ongoing"}
        ]
        
        # Filter relevant deals based on shopping list
        relevant_deals = []
        for deal in deals:
            # Check if any items in shopping list match deal category
            for category, items in self.shopping_lists.items():
                if items and not all(item["purchased"] for item in items):
                    relevant_deals.append(deal)
                    break
        
        return relevant_deals
    
    async def track_spending(self):
        """Track spending patterns and budget"""
        spending_data = []
        total_spent = 0
        
        for category, items in self.shopping_lists.items():
            category_spent = 0
            purchased_items = [item for item in items if item["purchased"]]
            
            for item in purchased_items:
                item_cost = item["estimated_price"] * item["quantity"]
                category_spent += item_cost
                total_spent += item_cost
            
            if purchased_items:
                spending_data.append({
                    "category": category,
                    "items_purchased": len(purchased_items),
                    "amount_spent": round(category_spent, 2),
                    "avg_item_cost": round(category_spent / len(purchased_items), 2)
                })
        
        # Budget analysis
        monthly_budget = self.config.get("user_preferences.budget_range.max", 500) * 4  # Assume monthly budget
        budget_used = (total_spent / monthly_budget) * 100 if monthly_budget > 0 else 0
        
        return {
            "total_spent": round(total_spent, 2),
            "monthly_budget": monthly_budget,
            "budget_used_percent": round(budget_used, 1),
            "category_breakdown": spending_data,
            "budget_status": "On track" if budget_used < 80 else "Over budget" if budget_used > 100 else "Approaching limit"
        }
    
    async def suggest_bulk_purchases(self):
        """Suggest items for bulk purchasing"""
        suggestions = []
        
        # Items that are frequently purchased
        frequent_items = ["toilet_paper", "detergent", "rice", "pasta", "canned_goods"]
        
        for item in frequent_items:
            if item in self.price_database:
                regular_price = list(self.price_database[item].values())[0]
                bulk_savings = regular_price * 0.15  # Assume 15% savings for bulk
                
                suggestions.append({
                    "item": item,
                    "regular_price": regular_price,
                    "bulk_price": round(regular_price - bulk_savings, 2),
                    "savings": round(bulk_savings, 2),
                    "reason": "Frequently used non-perishable item"
                })
        
        return suggestions
    
    async def execute(self):
        """Execute shopping assistant tasks"""
        try:
            self.logger.info("Starting shopping assistant tasks...")
            
            # Get shopping route optimization
            route_optimization = await self.optimize_shopping_route()
            
            # Get deals and coupons
            deals = await self.get_deals_and_coupons()
            
            # Track spending
            spending_analysis = await self.track_spending()
            
            # Get bulk purchase suggestions
            bulk_suggestions = await self.suggest_bulk_purchases()
            
            # Count items in lists
            total_items = sum(len(items) for items in self.shopping_lists.values())
            pending_items = sum(len([item for item in items if not item["purchased"]]) 
                              for items in self.shopping_lists.values())
            
            result = {
                "status": "success",
                "message": "Shopping assistant tasks completed successfully!",
                "data": {
                    "total_items_in_lists": total_items,
                    "pending_purchases": pending_items,
                    "stores_to_visit": route_optimization.get("stores_to_visit", 0),
                    "estimated_savings": route_optimization.get("estimated_savings", 0),
                    "active_deals": len(deals),
                    "budget_status": spending_analysis.get("budget_status", "Unknown")
                }
            }
            
            # Save detailed shopping data
            shopping_file = f"data/shopping_summary_{datetime.now().strftime('%Y%m%d')}.json"
            detailed_data = {
                "shopping_lists": self.shopping_lists,
                "route_optimization": route_optimization,
                "deals_and_coupons": deals,
                "spending_analysis": spending_analysis,
                "bulk_suggestions": bulk_suggestions,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(shopping_file, 'w') as f:
                json.dump(detailed_data, f, indent=2)
            
            self.logger.info("Shopping assistant tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in shopping assistant tasks: {str(e)}")
            return {"status": "error", "message": f"Shopping assistant failed: {str(e)}"}