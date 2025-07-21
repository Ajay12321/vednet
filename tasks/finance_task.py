"""
Personal Finance Management Task Manager
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.config import Config
from utils.logger import setup_logger

class FinanceManager:
    """Manages personal finance tracking and budget management"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger("finance")
        self.financial_data = self._load_financial_data()
        self.budget_categories = self._load_budget_categories()
        self.financial_goals = self._load_financial_goals()
    
    def _load_financial_data(self):
        """Load existing financial data"""
        try:
            with open("data/financial_data.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"transactions": [], "accounts": [], "investments": []}
    
    def _load_budget_categories(self):
        """Load budget categories with limits"""
        return {
            "housing": {"limit": 1500, "essential": True},
            "food": {"limit": 600, "essential": True},
            "transportation": {"limit": 400, "essential": True},
            "utilities": {"limit": 200, "essential": True},
            "entertainment": {"limit": 300, "essential": False},
            "shopping": {"limit": 400, "essential": False},
            "healthcare": {"limit": 200, "essential": True},
            "education": {"limit": 150, "essential": False},
            "savings": {"limit": 500, "essential": True}
        }
    
    def _load_financial_goals(self):
        """Load financial goals"""
        return {
            "emergency_fund": {"target": 10000, "current": 7500, "deadline": "2024-12-31"},
            "vacation": {"target": 3000, "current": 1200, "deadline": "2024-06-30"},
            "new_car": {"target": 25000, "current": 5000, "deadline": "2025-03-31"},
            "retirement": {"target": 100000, "current": 35000, "deadline": "2030-12-31"}
        }
    
    async def add_transaction(self, amount: float, category: str, description: str, transaction_type: str = "expense"):
        """Add a financial transaction"""
        transaction = {
            "id": f"txn_{random.randint(1000, 9999)}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "amount": abs(amount),
            "category": category,
            "description": description,
            "type": transaction_type,  # expense, income, transfer
            "created_at": datetime.now().isoformat()
        }
        
        self.financial_data["transactions"].append(transaction)
        await self._save_financial_data()
        
        return transaction
    
    async def _save_financial_data(self):
        """Save financial data to file"""
        with open("data/financial_data.json", 'w') as f:
            json.dump(self.financial_data, f, indent=2)
    
    async def analyze_monthly_budget(self):
        """Analyze current month's budget performance"""
        current_month = datetime.now().strftime("%Y-%m")
        
        # Filter transactions for current month
        monthly_transactions = [
            t for t in self.financial_data["transactions"]
            if t["date"].startswith(current_month) and t["type"] == "expense"
        ]
        
        # Calculate spending by category
        category_spending = {}
        total_spent = 0
        
        for transaction in monthly_transactions:
            category = transaction["category"]
            amount = transaction["amount"]
            
            category_spending[category] = category_spending.get(category, 0) + amount
            total_spent += amount
        
        # Compare with budget limits
        budget_analysis = {}
        total_budget = sum(cat["limit"] for cat in self.budget_categories.values())
        
        for category, budget_info in self.budget_categories.items():
            spent = category_spending.get(category, 0)
            limit = budget_info["limit"]
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            budget_analysis[category] = {
                "spent": spent,
                "limit": limit,
                "remaining": max(0, limit - spent),
                "percentage": round(percentage, 1),
                "status": "over" if spent > limit else "warning" if percentage > 80 else "good"
            }
        
        return {
            "total_spent": round(total_spent, 2),
            "total_budget": total_budget,
            "budget_used_percentage": round((total_spent / total_budget) * 100, 1),
            "category_analysis": budget_analysis,
            "transaction_count": len(monthly_transactions)
        }
    
    async def track_financial_goals(self):
        """Track progress toward financial goals"""
        goal_progress = {}
        
        for goal_name, goal_info in self.financial_goals.items():
            target = goal_info["target"]
            current = goal_info["current"]
            deadline = datetime.strptime(goal_info["deadline"], "%Y-%m-%d")
            
            progress_percentage = (current / target) * 100
            days_remaining = (deadline - datetime.now()).days
            
            # Calculate required monthly savings
            months_remaining = max(1, days_remaining / 30)
            required_monthly = (target - current) / months_remaining
            
            goal_progress[goal_name] = {
                "target": target,
                "current": current,
                "remaining": target - current,
                "progress_percentage": round(progress_percentage, 1),
                "days_remaining": days_remaining,
                "required_monthly_savings": round(required_monthly, 2),
                "status": "on_track" if progress_percentage >= 50 else "behind"
            }
        
        return goal_progress
    
    async def analyze_spending_patterns(self):
        """Analyze spending patterns and trends"""
        if not self.financial_data["transactions"]:
            return {"message": "No transaction data to analyze"}
        
        # Last 30 days analysis
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_transactions = [
            t for t in self.financial_data["transactions"]
            if datetime.strptime(t["date"], "%Y-%m-%d") >= thirty_days_ago and t["type"] == "expense"
        ]
        
        # Daily spending average
        if recent_transactions:
            total_recent_spending = sum(t["amount"] for t in recent_transactions)
            avg_daily_spending = total_recent_spending / 30
        else:
            avg_daily_spending = 0
        
        # Category preferences
        category_totals = {}
        for transaction in recent_transactions:
            category = transaction["category"]
            category_totals[category] = category_totals.get(category, 0) + transaction["amount"]
        
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Day of week spending
        weekday_spending = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        
        for transaction in recent_transactions:
            date = datetime.strptime(transaction["date"], "%Y-%m-%d")
            weekday = date.strftime("%A")
            weekday_spending[weekday] += transaction["amount"]
        
        highest_spending_day = max(weekday_spending, key=weekday_spending.get)
        
        return {
            "avg_daily_spending": round(avg_daily_spending, 2),
            "total_transactions_30_days": len(recent_transactions),
            "top_spending_categories": top_categories,
            "highest_spending_day": highest_spending_day,
            "spending_insights": [
                "Track discretionary spending more closely",
                "Consider automating savings",
                "Review recurring subscriptions"
            ]
        }
    
    async def get_savings_recommendations(self):
        """Get personalized savings recommendations"""
        budget_analysis = await self.analyze_monthly_budget()
        recommendations = []
        
        # Analyze budget categories for savings opportunities
        for category, analysis in budget_analysis["category_analysis"].items():
            if not self.budget_categories[category]["essential"] and analysis["percentage"] > 50:
                potential_savings = analysis["spent"] * 0.2  # Suggest 20% reduction
                recommendations.append({
                    "category": category,
                    "current_spending": analysis["spent"],
                    "suggested_reduction": round(potential_savings, 2),
                    "reason": f"High spending in non-essential category",
                    "difficulty": "medium"
                })
        
        # General recommendations
        general_tips = [
            {"tip": "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings", "potential_savings": 200},
            {"tip": "Cancel unused subscriptions", "potential_savings": 50},
            {"tip": "Cook more meals at home", "potential_savings": 150},
            {"tip": "Use cashback credit cards responsibly", "potential_savings": 30},
            {"tip": "Negotiate bills (phone, internet, insurance)", "potential_savings": 75}
        ]
        
        recommendations.extend(random.sample(general_tips, 3))
        
        return recommendations
    
    async def generate_financial_report(self):
        """Generate comprehensive financial report"""
        budget_analysis = await self.analyze_monthly_budget()
        goal_progress = await self.track_financial_goals()
        spending_patterns = await self.analyze_spending_patterns()
        savings_recommendations = await self.get_savings_recommendations()
        
        # Calculate net worth (simplified)
        total_savings = sum(goal["current"] for goal in self.financial_goals.values())
        monthly_expenses = budget_analysis["total_spent"]
        
        # Financial health score (0-100)
        budget_score = max(0, 100 - budget_analysis["budget_used_percentage"])
        goal_score = sum(goal["progress_percentage"] for goal in goal_progress.values()) / len(goal_progress)
        financial_health_score = (budget_score + goal_score) / 2
        
        return {
            "financial_health_score": round(financial_health_score, 1),
            "total_savings": round(total_savings, 2),
            "monthly_expenses": monthly_expenses,
            "budget_performance": budget_analysis,
            "goal_progress": goal_progress,
            "spending_insights": spending_patterns,
            "savings_opportunities": savings_recommendations[:3],
            "recommendations": [
                "Continue building emergency fund" if goal_progress["emergency_fund"]["progress_percentage"] < 75 else "Emergency fund looking good!",
                "Consider increasing retirement contributions",
                "Review and optimize investment portfolio"
            ]
        }
    
    async def simulate_daily_transactions(self):
        """Simulate some daily transactions for demo purposes"""
        sample_transactions = [
            {"amount": 12.50, "category": "food", "description": "Coffee shop"},
            {"amount": 35.00, "category": "food", "description": "Grocery shopping"},
            {"amount": 8.99, "category": "entertainment", "description": "Streaming service"},
            {"amount": 45.00, "category": "transportation", "description": "Gas"},
            {"amount": 25.00, "category": "shopping", "description": "Online purchase"}
        ]
        
        # Add random transaction
        transaction = random.choice(sample_transactions)
        await self.add_transaction(
            transaction["amount"],
            transaction["category"],
            transaction["description"]
        )
        
        return transaction
    
    async def get_investment_overview(self):
        """Get basic investment overview"""
        # Simulate investment data
        investments = {
            "stocks": {"value": 15000, "change_today": 1.2, "allocation": 60},
            "bonds": {"value": 5000, "change_today": 0.3, "allocation": 20},
            "real_estate": {"value": 8000, "change_today": 0.8, "allocation": 20}
        }
        
        total_value = sum(inv["value"] for inv in investments.values())
        total_change = sum(inv["value"] * (inv["change_today"] / 100) for inv in investments.values())
        
        return {
            "total_portfolio_value": total_value,
            "today_change": round(total_change, 2),
            "today_change_percentage": round((total_change / total_value) * 100, 2),
            "asset_allocation": investments
        }
    
    async def execute(self):
        """Execute finance management tasks"""
        try:
            self.logger.info("Starting finance management tasks...")
            
            # Simulate a daily transaction
            daily_transaction = await self.simulate_daily_transactions()
            
            # Analyze monthly budget
            budget_analysis = await self.analyze_monthly_budget()
            
            # Track financial goals
            goal_progress = await self.track_financial_goals()
            
            # Analyze spending patterns
            spending_patterns = await self.analyze_spending_patterns()
            
            # Get savings recommendations
            savings_recommendations = await self.get_savings_recommendations()
            
            # Get investment overview
            investment_overview = await self.get_investment_overview()
            
            # Generate financial report
            financial_report = await self.generate_financial_report()
            
            result = {
                "status": "success",
                "message": "Finance management tasks completed successfully!",
                "data": {
                    "budget_health": budget_analysis["budget_used_percentage"],
                    "financial_health_score": financial_report["financial_health_score"],
                    "total_savings": financial_report["total_savings"],
                    "active_goals": len(goal_progress),
                    "savings_opportunities": len(savings_recommendations),
                    "portfolio_value": investment_overview["total_portfolio_value"]
                }
            }
            
            # Save detailed financial data
            finance_file = f"data/finance_summary_{datetime.now().strftime('%Y%m%d')}.json"
            detailed_data = {
                "budget_analysis": budget_analysis,
                "goal_progress": goal_progress,
                "spending_patterns": spending_patterns,
                "savings_recommendations": savings_recommendations,
                "investment_overview": investment_overview,
                "financial_report": financial_report,
                "daily_transaction": daily_transaction,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(finance_file, 'w') as f:
                json.dump(detailed_data, f, indent=2)
            
            self.logger.info("Finance management tasks completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in finance management tasks: {str(e)}")
            return {"status": "error", "message": f"Finance management failed: {str(e)}"}