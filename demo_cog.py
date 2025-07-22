#!/usr/bin/env python3
"""
Cog AI Assistant Demo
A simplified version that demonstrates the core functionality without external dependencies
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class SimpleCogDemo:
    """Simplified Cog demo without external dependencies"""
    
    def __init__(self):
        self.name = "Cog"
        self.version = "1.0.0 (Demo)"
        
        # Intent patterns for simple matching
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bcog\b.*\b(hi|hello|hey)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|farewell|exit|quit)\b'
            ],
            'help': [
                r'\b(help|what can you do|capabilities|commands)\b'
            ],
            'food_order': [
                r'\border.*\b(food|pizza|burger|meal|lunch|dinner)\b',
                r'\b(swiggy|zomato|ubereats|doordash).*order\b',
                r'\bi want.*\b(pizza|food|meal)\b'
            ],
            'movie_booking': [
                r'\book.*\b(movie|ticket|film|cinema)\b',
                r'\b(bookmyshow|movie ticket|cinema ticket)\b',
                r'\bwatch.*\b(movie|film)\b'
            ],
            'shopping': [
                r'\bbuy.*\b(dress|clothes|shirt|shoes|book)\b',
                r'\border.*\b(amazon|flipkart|myntra)\b',
                r'\bi need.*\b(dress|clothes|item)\b'
            ],
            'reminder': [
                r'\bremind me\b',
                r'\bset.*reminder\b',
                r'\bschedule.*\b'
            ],
            'weather': [
                r'\bweather\b',
                r'\btemperature\b',
                r'\bhow.*\b(hot|cold|warm)\b'
            ],
            'news': [
                r'\bnews\b',
                r'\blatest.*news\b',
                r'\bwhat.*happening\b'
            ]
        }
        
        print(f"🤖 {self.name} {self.version} initialized")
    
    def analyze_command(self, command: str) -> Dict[str, Any]:
        """Analyze command to determine intent"""
        command_lower = command.lower().strip()
        
        best_intent = "general_query"
        best_confidence = 0.0
        parameters = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command_lower, re.IGNORECASE):
                    confidence = 0.8
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
        
        # Extract basic parameters
        if best_intent == 'food_order':
            parameters = self._extract_food_parameters(command_lower)
        elif best_intent == 'movie_booking':
            parameters = self._extract_movie_parameters(command_lower)
        elif best_intent == 'shopping':
            parameters = self._extract_shopping_parameters(command_lower)
        elif best_intent == 'reminder':
            parameters = self._extract_reminder_parameters(command_lower)
        
        return {
            'intent': best_intent,
            'parameters': parameters,
            'confidence': best_confidence
        }
    
    def _extract_food_parameters(self, command: str) -> Dict[str, Any]:
        """Extract food ordering parameters"""
        parameters = {}
        
        food_items = ['pizza', 'burger', 'biryani', 'chicken', 'chinese', 'indian', 'pasta']
        for item in food_items:
            if item in command:
                parameters['food_type'] = item
                break
        
        platforms = ['swiggy', 'zomato', 'ubereats', 'doordash']
        for platform in platforms:
            if platform in command:
                parameters['platform'] = platform
                break
        
        return parameters
    
    def _extract_movie_parameters(self, command: str) -> Dict[str, Any]:
        """Extract movie booking parameters"""
        parameters = {}
        
        movie_keywords = ['avengers', 'batman', 'spider', 'movie']
        for keyword in movie_keywords:
            if keyword in command:
                parameters['movie_name'] = keyword.title()
                break
        
        return parameters
    
    def _extract_shopping_parameters(self, command: str) -> Dict[str, Any]:
        """Extract shopping parameters"""
        parameters = {}
        
        items = ['dress', 'shirt', 'shoes', 'book', 'phone', 'laptop']
        for item in items:
            if item in command:
                parameters['item_type'] = item
                break
        
        colors = ['red', 'blue', 'black', 'white', 'green']
        for color in colors:
            if color in command:
                parameters['color'] = color
                break
        
        platforms = ['amazon', 'flipkart', 'myntra']
        for platform in platforms:
            if platform in command:
                parameters['platform'] = platform
                break
        
        return parameters
    
    def _extract_reminder_parameters(self, command: str) -> Dict[str, Any]:
        """Extract reminder parameters"""
        parameters = {}
        
        if 'remind me to' in command:
            parts = command.split('remind me to')
            if len(parts) > 1:
                parameters['reminder_text'] = parts[1].strip()
        
        return parameters
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """Process a user command"""
        print(f"\n🎯 Processing: '{command}'")
        
        # Analyze command
        analysis = self.analyze_command(command)
        intent = analysis['intent']
        parameters = analysis['parameters']
        
        print(f"   Intent: {intent} (confidence: {analysis['confidence']:.2f})")
        if parameters:
            print(f"   Parameters: {parameters}")
        
        # Execute based on intent
        if intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'goodbye':
            return self._handle_goodbye()
        elif intent == 'help':
            return self._handle_help()
        elif intent == 'food_order':
            return self._handle_food_order(parameters)
        elif intent == 'movie_booking':
            return self._handle_movie_booking(parameters)
        elif intent == 'shopping':
            return self._handle_shopping(parameters)
        elif intent == 'reminder':
            return self._handle_reminder(parameters)
        elif intent == 'weather':
            return self._handle_weather()
        elif intent == 'news':
            return self._handle_news()
        else:
            return self._handle_general_query(command)
    
    def _handle_greeting(self) -> Dict[str, Any]:
        """Handle greeting"""
        responses = [
            "Hello! I'm Cog, your AI assistant. How can I help you today?",
            "Hi there! What can I do for you?",
            "Hello! Ready to assist you with any task."
        ]
        import random
        response = random.choice(responses)
        return {"success": True, "response": response}
    
    def _handle_goodbye(self) -> Dict[str, Any]:
        """Handle goodbye"""
        return {"success": True, "response": "Goodbye! Have a great day!", "exit": True}
    
    def _handle_help(self) -> Dict[str, Any]:
        """Handle help request"""
        help_text = """
🤖 Cog AI Assistant - Available Commands:

🍕 Food Ordering:
   - "Order pizza from Swiggy"
   - "I want biryani from Zomato"

🎬 Movie Booking:
   - "Book movie tickets for Avengers"
   - "Movie ticket for tonight"

🛒 Shopping:
   - "Buy a red dress from Amazon"
   - "Order phone from Flipkart"

📅 Reminders:
   - "Remind me to call mom"
   - "Set reminder for meeting"

🌤️ Information:
   - "What's the weather?"
   - "Get latest news"

💬 General:
   - "Help" - Show this help
   - "Exit" - Quit the demo

Try any of these commands!
        """
        return {"success": True, "response": help_text}
    
    def _handle_food_order(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle food ordering"""
        food_type = parameters.get('food_type', 'food')
        platform = parameters.get('platform', 'Swiggy')
        
        order_id = f"{platform.upper()}_{uuid.uuid4().hex[:8].upper()}"
        
        response = f"""
🍕 Food Order Placed!

Platform: {platform.title()}
Item: {food_type.title()}
Order ID: {order_id}
Estimated Delivery: 30-45 minutes
Total: ₹299

Your order has been placed successfully!
        """
        
        return {
            "success": True,
            "response": response,
            "order_details": {
                "platform": platform,
                "item": food_type,
                "order_id": order_id,
                "total": "₹299"
            }
        }
    
    def _handle_movie_booking(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle movie booking"""
        movie_name = parameters.get('movie_name', 'Latest Movie')
        
        booking_id = f"BMS_{uuid.uuid4().hex[:8].upper()}"
        
        response = f"""
🎬 Movie Ticket Booked!

Movie: {movie_name}
Theater: PVR Cinemas
Show Time: 7:00 PM
Seats: F12, F13
Booking ID: {booking_id}
Total: ₹400

Enjoy your movie!
        """
        
        return {
            "success": True,
            "response": response,
            "booking_details": {
                "movie": movie_name,
                "theater": "PVR Cinemas",
                "booking_id": booking_id,
                "total": "₹400"
            }
        }
    
    def _handle_shopping(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle shopping"""
        item_type = parameters.get('item_type', 'item')
        color = parameters.get('color', '')
        platform = parameters.get('platform', 'Amazon')
        
        item_description = f"{color} {item_type}".strip()
        order_id = f"{platform.upper()}_{uuid.uuid4().hex[:8].upper()}"
        
        response = f"""
🛒 Shopping Success!

Platform: {platform.title()}
Item: {item_description.title()}
Order ID: {order_id}
Price: ₹1,299
Delivery: Tomorrow
Status: Added to Cart

Ready to checkout when you are!
        """
        
        return {
            "success": True,
            "response": response,
            "shopping_details": {
                "platform": platform,
                "item": item_description,
                "order_id": order_id,
                "price": "₹1,299"
            }
        }
    
    def _handle_reminder(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle reminder setting"""
        reminder_text = parameters.get('reminder_text', 'general reminder')
        
        response = f"""
📅 Reminder Set!

Reminder: {reminder_text.title()}
Time: 1 hour from now
Status: Active

I'll remind you when it's time!
        """
        
        return {
            "success": True,
            "response": response,
            "reminder": {
                "text": reminder_text,
                "time": "1 hour from now"
            }
        }
    
    def _handle_weather(self) -> Dict[str, Any]:
        """Handle weather query"""
        response = """
🌤️ Weather Update

Location: Current Location
Temperature: 24°C
Condition: Partly Cloudy
Humidity: 65%
Wind: 10 km/h

Perfect weather for outdoor activities!
        """
        
        return {"success": True, "response": response}
    
    def _handle_news(self) -> Dict[str, Any]:
        """Handle news query"""
        response = """
📰 Latest News

• Tech stocks rise amid AI optimism
• New breakthrough in renewable energy
• Global climate summit concludes successfully

Stay informed, stay ahead!
        """
        
        return {"success": True, "response": response}
    
    def _handle_general_query(self, command: str) -> Dict[str, Any]:
        """Handle general queries"""
        responses = [
            "I understand you're asking about something, but I'm not sure exactly what. Could you be more specific?",
            "That's an interesting question! I'm a demo version, so my responses are limited. Try asking about food, movies, shopping, or weather!",
            "I'd love to help with that! For now, I can assist with ordering food, booking movies, shopping, setting reminders, and getting weather/news updates."
        ]
        
        import random
        response = random.choice(responses)
        
        return {"success": True, "response": response}

def main():
    """Main demo function"""
    print("=" * 60)
    print("🤖 Welcome to Cog AI Assistant Demo!")
    print("=" * 60)
    print("This is a simplified demo version showcasing core functionality.")
    print("Type 'help' to see available commands or 'exit' to quit.")
    print("=" * 60)
    
    # Initialize Cog
    cog = SimpleCogDemo()
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Process command
            result = cog.process_command(user_input)
            
            # Display response
            print(f"🤖 Cog: {result['response']}")
            
            # Check for exit
            if result.get('exit'):
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for trying Cog AI Assistant Demo!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type 'help' for available commands.")

if __name__ == "__main__":
    main()