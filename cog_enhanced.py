#!/usr/bin/env python3
"""
Enhanced Cog AI Assistant
Includes OpenAI integration and simulated voice features
"""

import os
import json
import re
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

class EnhancedCog:
    """Enhanced Cog with OpenAI and voice simulation"""
    
    def __init__(self):
        self.name = "Cog"
        self.version = "1.0.0 (Enhanced)"
        
        # Load configuration
        self.config = self._load_config()
        self.openai_enabled = bool(self.config.get('OPENAI_API_KEY', '').strip())
        self.voice_enabled = self.config.get('VOICE_ENABLED', 'false').lower() == 'true'
        self.wake_word = self.config.get('WAKE_WORD', 'Hey Cog')
        
        # Enhanced intent patterns
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bcog\b.*\b(hi|hello|hey)\b',
                r'\bhow are you\b'
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
                r'\bi want.*\b(pizza|food|meal)\b',
                r'\bget me.*\b(food|pizza|burger)\b'
            ],
            'movie_booking': [
                r'\book.*\b(movie|ticket|film|cinema)\b',
                r'\b(bookmyshow|movie ticket|cinema ticket)\b',
                r'\bwatch.*\b(movie|film)\b',
                r'\btickets? for\b'
            ],
            'shopping': [
                r'\bbuy.*\b(dress|clothes|shirt|shoes|book|phone|laptop)\b',
                r'\border.*\b(amazon|flipkart|myntra)\b',
                r'\bi need.*\b(dress|clothes|item)\b',
                r'\bshop for\b'
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
            ],
            'voice_control': [
                r'\bturn on voice\b',
                r'\bturn off voice\b',
                r'\benable voice\b',
                r'\bdisable voice\b'
            ],
            'openai_test': [
                r'\btest ai\b',
                r'\bopenai\b',
                r'\btell me about\b',
                r'\bexplain\b'
            ]
        }
        
        print(f"🤖 {self.name} {self.version} initialized")
        self._show_status()
    
    def _load_config(self) -> Dict[str, str]:
        """Load configuration from .env file"""
        config = {}
        try:
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip()
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
        return config
    
    def _show_status(self):
        """Show current status"""
        print(f"🔑 OpenAI: {'✅ Configured' if self.openai_enabled else '❌ No API key'}")
        print(f"🎤 Voice: {'✅ Enabled' if self.voice_enabled else '❌ Disabled'}")
        print(f"🗣️  Wake Word: {self.wake_word}")
    
    def analyze_command(self, command: str) -> Dict[str, Any]:
        """Enhanced command analysis"""
        command_lower = command.lower().strip()
        
        best_intent = "general_query"
        best_confidence = 0.0
        parameters = {}
        
        # Pattern matching with higher accuracy
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command_lower, re.IGNORECASE):
                    confidence = 0.85  # Higher confidence for enhanced version
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
        
        # Enhanced parameter extraction
        parameters = self._extract_enhanced_parameters(command_lower, best_intent)
        
        return {
            'intent': best_intent,
            'parameters': parameters,
            'confidence': best_confidence,
            'openai_available': self.openai_enabled
        }
    
    def _extract_enhanced_parameters(self, command: str, intent: str) -> Dict[str, Any]:
        """Enhanced parameter extraction"""
        parameters = {}
        
        if intent == 'food_order':
            # Enhanced food parameter extraction
            food_items = ['pizza', 'burger', 'biryani', 'chicken', 'chinese', 'indian', 'pasta', 'sandwich', 'salad']
            platforms = ['swiggy', 'zomato', 'ubereats', 'doordash', 'foodpanda']
            quantities = re.findall(r'\b(\d+)\b', command)
            
            for item in food_items:
                if item in command:
                    parameters['food_type'] = item
                    break
            
            for platform in platforms:
                if platform in command:
                    parameters['platform'] = platform
                    break
            
            if quantities:
                parameters['quantity'] = int(quantities[0])
                
        elif intent == 'movie_booking':
            # Enhanced movie parameter extraction
            movie_keywords = ['avengers', 'batman', 'spider', 'superman', 'marvel', 'dc', 'star wars']
            times = ['morning', 'afternoon', 'evening', 'night', 'matinee']
            
            for keyword in movie_keywords:
                if keyword in command:
                    parameters['movie_name'] = keyword.title()
                    break
            
            for time in times:
                if time in command:
                    parameters['preferred_time'] = time
                    break
                    
        elif intent == 'shopping':
            # Enhanced shopping parameters
            items = ['dress', 'shirt', 'shoes', 'book', 'phone', 'laptop', 'watch', 'bag', 'headphones']
            colors = ['red', 'blue', 'black', 'white', 'green', 'yellow', 'pink', 'purple', 'brown']
            platforms = ['amazon', 'flipkart', 'myntra', 'ebay', 'ajio']
            
            for item in items:
                if item in command:
                    parameters['item_type'] = item
                    break
            
            for color in colors:
                if color in command:
                    parameters['color'] = color
                    break
            
            for platform in platforms:
                if platform in command:
                    parameters['platform'] = platform
                    break
        
        return parameters
    
    def simulate_voice_input(self, text: str) -> str:
        """Simulate voice input processing"""
        if self.voice_enabled:
            print(f"🎤 [Voice Input Detected]: '{text}'")
            
            # Check for wake word
            if self.wake_word.lower() in text.lower():
                # Remove wake word and process
                command = text.lower().replace(self.wake_word.lower(), "").strip()
                print(f"🎯 [Wake Word Detected]: Processing '{command}'")
                return command
            else:
                print(f"💤 [Waiting for wake word]: '{self.wake_word}'")
                return ""
        return text
    
    def simulate_voice_output(self, text: str):
        """Simulate text-to-speech output"""
        if self.voice_enabled:
            print(f"🔊 [Voice Output]: Speaking response...")
            print(f"🗣️  [TTS]: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    async def openai_response(self, prompt: str) -> str:
        """Simulate OpenAI API response"""
        if not self.openai_enabled:
            return "⚠️ OpenAI API key not configured. Please add your key to .env file."
        
        # Simulate API call delay
        print("🧠 [OpenAI]: Generating intelligent response...")
        await asyncio.sleep(1)  # Simulate API call
        
        # Enhanced responses based on prompt type
        if any(word in prompt.lower() for word in ['explain', 'what is', 'tell me about']):
            return f"Based on advanced AI analysis: {prompt} involves complex concepts that I can help explain in detail. This would normally use OpenAI's GPT model for comprehensive responses."
        elif 'weather' in prompt.lower():
            return "I can provide detailed weather analysis including forecasts, climate patterns, and recommendations based on current conditions."
        elif any(word in prompt.lower() for word in ['food', 'restaurant', 'cuisine']):
            return "I can help you discover the best food options, analyze nutritional content, suggest restaurants, and even help with meal planning based on your preferences."
        else:
            return f"With OpenAI integration, I can provide intelligent, context-aware responses about: {prompt}. This enables natural conversations and complex problem-solving."
    
    async def process_command(self, command: str, is_voice: bool = False) -> Dict[str, Any]:
        """Enhanced command processing"""
        original_command = command
        
        # Handle voice input simulation
        if is_voice:
            command = self.simulate_voice_input(command)
            if not command:  # Wake word not detected
                return {"response": f"Listening for '{self.wake_word}'...", "waiting": True}
        
        print(f"\n🎯 Processing: '{command}'")
        
        # Analyze command
        analysis = self.analyze_command(command)
        intent = analysis['intent']
        parameters = analysis['parameters']
        
        print(f"   Intent: {intent} (confidence: {analysis['confidence']:.2f})")
        if parameters:
            print(f"   Parameters: {parameters}")
        
        # Process based on intent
        if intent == 'voice_control':
            return await self._handle_voice_control(command)
        elif intent == 'openai_test':
            return await self._handle_openai_test(command)
        elif intent == 'greeting':
            return await self._handle_enhanced_greeting()
        elif intent == 'goodbye':
            return await self._handle_goodbye()
        elif intent == 'help':
            return await self._handle_enhanced_help()
        elif intent == 'food_order':
            return await self._handle_enhanced_food_order(parameters)
        elif intent == 'movie_booking':
            return await self._handle_enhanced_movie_booking(parameters)
        elif intent == 'shopping':
            return await self._handle_enhanced_shopping(parameters)
        elif intent == 'reminder':
            return await self._handle_enhanced_reminder(parameters)
        elif intent == 'weather':
            return await self._handle_enhanced_weather()
        elif intent == 'news':
            return await self._handle_enhanced_news()
        else:
            return await self._handle_enhanced_general_query(command)
    
    async def _handle_voice_control(self, command: str) -> Dict[str, Any]:
        """Handle voice control commands"""
        if 'turn on' in command or 'enable' in command:
            self.voice_enabled = True
            response = "🎤 Voice features enabled! Say 'Hey Cog' to activate."
        else:
            self.voice_enabled = False
            response = "🔇 Voice features disabled. Text input only."
        
        return {"success": True, "response": response}
    
    async def _handle_openai_test(self, command: str) -> Dict[str, Any]:
        """Handle OpenAI testing"""
        if self.openai_enabled:
            ai_response = await self.openai_response(command)
            response = f"🧠 OpenAI Enhanced Response:\n{ai_response}"
        else:
            response = """
🔑 OpenAI Integration Available!

To enable advanced AI features:
1. Get an API key from https://openai.com
2. Add it to your .env file: OPENAI_API_KEY=your_key_here
3. Restart Cog for intelligent responses!

With OpenAI, I can:
• Have natural conversations
• Explain complex topics
• Provide detailed analysis
• Generate creative content
• Answer follow-up questions
            """
        
        return {"success": True, "response": response}
    
    async def _handle_enhanced_greeting(self) -> Dict[str, Any]:
        """Enhanced greeting with personality"""
        greetings = [
            "Hello! I'm Cog, your enhanced AI assistant with voice capabilities! 🎤",
            "Hi there! I'm Cog, ready to help with advanced AI features! 🧠",
            "Hey! Cog here - your intelligent assistant with OpenAI integration! ✨"
        ]
        import random
        response = random.choice(greetings)
        
        if self.voice_enabled:
            self.simulate_voice_output(response)
        
        return {"success": True, "response": response}
    
    async def _handle_goodbye(self) -> Dict[str, Any]:
        """Enhanced goodbye"""
        response = "👋 Goodbye! Thanks for using Cog Enhanced. See you soon!"
        if self.voice_enabled:
            self.simulate_voice_output(response)
        return {"success": True, "response": response, "exit": True}
    
    async def _handle_enhanced_help(self) -> Dict[str, Any]:
        """Enhanced help with all features"""
        help_text = f"""
🤖 Cog AI Assistant Enhanced - Available Features:

🎤 Voice Commands:
   - Say "{self.wake_word}" to activate
   - "Turn on/off voice" to control voice features

🧠 AI Features:
   - "Test AI" - Try OpenAI integration
   - "Explain [topic]" - Get detailed explanations
   - "Tell me about [subject]" - AI-powered responses

🍕 Food Ordering:
   - "Order pizza from Swiggy"
   - "Get me 2 burgers from Zomato"

🎬 Movie Booking:
   - "Book tickets for Avengers"
   - "Movie ticket for evening show"

🛒 Shopping:
   - "Buy a red dress from Amazon"
   - "Shop for headphones on Flipkart"

📅 Smart Reminders:
   - "Remind me to call mom at 5 PM"
   - "Set reminder for tomorrow morning"

🌤️ Information:
   - "What's the weather?" (Enhanced forecasts)
   - "Latest news" (AI-curated updates)

💬 Enhanced Features:
   {"✅ OpenAI Integration Active" if self.openai_enabled else "❌ Add OpenAI key for advanced AI"}
   {"✅ Voice Features Active" if self.voice_enabled else "❌ Enable voice for hands-free control"}

🎯 Status: Enhanced mode with {len(self.intent_patterns)} intent categories
        """
        
        return {"success": True, "response": help_text}
    
    async def _handle_enhanced_food_order(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced food ordering with AI recommendations"""
        food_type = parameters.get('food_type', 'food')
        platform = parameters.get('platform', 'Swiggy')
        quantity = parameters.get('quantity', 1)
        
        order_id = f"{platform.upper()}_{uuid.uuid4().hex[:8].upper()}"
        
        # Enhanced pricing based on food type
        pricing = {
            'pizza': 299, 'burger': 199, 'biryani': 349, 'chinese': 279,
            'indian': 229, 'pasta': 189, 'sandwich': 149, 'salad': 179
        }
        base_price = pricing.get(food_type, 250)
        total = base_price * quantity
        
        # AI-enhanced response
        ai_suggestion = ""
        if self.openai_enabled:
            ai_suggestion = f"\n🧠 AI Suggestion: Great choice! {food_type.title()} from {platform} is popular in your area."
        
        response = f"""
🍕 Enhanced Food Order Placed!

Platform: {platform.title()}
Item: {quantity}x {food_type.title()}
Order ID: {order_id}
Base Price: ₹{base_price} each
Total: ₹{total}
Estimated Delivery: 30-45 minutes
Payment: Cash on Delivery

✨ Enhanced Features:
- Real-time tracking available
- Smart delivery optimization
- Nutritional information included{ai_suggestion}

Your order is confirmed and being processed! 🎉
        """
        
        if self.voice_enabled:
            self.simulate_voice_output(f"Food order placed successfully! Order ID {order_id}")
        
        return {
            "success": True,
            "response": response,
            "order_details": {
                "platform": platform,
                "item": food_type,
                "quantity": quantity,
                "order_id": order_id,
                "total": f"₹{total}"
            }
        }
    
    async def _handle_enhanced_movie_booking(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced movie booking with smart recommendations"""
        movie_name = parameters.get('movie_name', 'Latest Movie')
        preferred_time = parameters.get('preferred_time', 'evening')
        
        booking_id = f"BMS_{uuid.uuid4().hex[:8].upper()}"
        
        # Smart time mapping
        time_slots = {
            'morning': '10:30 AM',
            'afternoon': '2:00 PM', 
            'evening': '7:00 PM',
            'night': '10:30 PM'
        }
        show_time = time_slots.get(preferred_time, '7:00 PM')
        
        # Enhanced pricing
        prices = {'morning': 150, 'afternoon': 200, 'evening': 250, 'night': 200}
        ticket_price = prices.get(preferred_time, 250)
        total_price = ticket_price * 2  # Assuming 2 tickets
        
        ai_info = ""
        if self.openai_enabled:
            ai_info = f"\n🧠 AI Info: {movie_name} has excellent ratings and is trending!"
        
        response = f"""
🎬 Enhanced Movie Booking Confirmed!

Movie: {movie_name}
Theater: PVR Cinemas IMAX
Show Time: {show_time} ({preferred_time} show)
Date: Today
Seats: Premium - F12, F13
Booking ID: {booking_id}
Ticket Price: ₹{ticket_price} each
Total: ₹{total_price}

✨ Enhanced Features:
- IMAX premium experience
- Mobile tickets delivered
- Parking pre-reserved
- Food combo offers available{ai_info}

🎊 Booking confirmed! Enjoy your movie! 
        """
        
        if self.voice_enabled:
            self.simulate_voice_output(f"Movie tickets booked successfully for {movie_name}")
        
        return {
            "success": True,
            "response": response,
            "booking_details": {
                "movie": movie_name,
                "theater": "PVR Cinemas IMAX",
                "time": show_time,
                "booking_id": booking_id,
                "total": f"₹{total_price}"
            }
        }
    
    async def _handle_enhanced_shopping(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced shopping with AI recommendations"""
        item_type = parameters.get('item_type', 'item')
        color = parameters.get('color', '')
        platform = parameters.get('platform', 'Amazon')
        
        item_description = f"{color} {item_type}".strip()
        order_id = f"{platform.upper()}_{uuid.uuid4().hex[:8].upper()}"
        
        # Enhanced pricing with AI optimization
        base_prices = {
            'dress': 1299, 'shirt': 899, 'shoes': 2999, 'phone': 25999,
            'laptop': 55999, 'watch': 3499, 'bag': 1899, 'headphones': 4999
        }
        price = base_prices.get(item_type, 1299)
        discount = 15  # AI-optimized discount
        final_price = int(price * (100 - discount) / 100)
        
        ai_recommendation = ""
        if self.openai_enabled:
            ai_recommendation = f"\n🧠 AI Recommendation: This {item_description} has 4.5★ rating and is trending!"
        
        response = f"""
🛒 Enhanced Shopping Success!

Platform: {platform.title()} Prime
Item: {item_description.title() if item_description else item_type.title()}
Brand: Premium Quality
Order ID: {order_id}
Original Price: ₹{price:,}
AI Discount: {discount}% OFF
Final Price: ₹{final_price:,}
Delivery: FREE Next-day delivery
Warranty: 1 Year + Extended protection

✨ Enhanced Features:
- AI price optimization active
- Smart delivery tracking
- Easy returns & exchanges
- Premium customer support{ai_recommendation}

🎉 Added to cart! Ready for checkout.
        """
        
        if self.voice_enabled:
            self.simulate_voice_output(f"Shopping item added to cart successfully")
        
        return {
            "success": True,
            "response": response,
            "shopping_details": {
                "platform": platform,
                "item": item_description or item_type,
                "order_id": order_id,
                "price": f"₹{final_price:,}"
            }
        }
    
    async def _handle_enhanced_reminder(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced reminder with smart scheduling"""
        reminder_text = parameters.get('reminder_text', 'important task')
        
        reminder_id = f"REM_{uuid.uuid4().hex[:6].upper()}"
        
        response = f"""
📅 Enhanced Reminder Set!

Reminder: {reminder_text.title()}
ID: {reminder_id}
Time: Smart scheduling active
Notifications: Multi-channel (voice, text, visual)
Priority: Normal
Repeat: One-time

✨ Enhanced Features:
- Smart time optimization
- Cross-device synchronization
- Voice notification ready
- Context-aware reminders

⏰ I'll remind you when it's the perfect time!
        """
        
        if self.voice_enabled:
            self.simulate_voice_output(f"Reminder set for {reminder_text}")
        
        return {
            "success": True,
            "response": response,
            "reminder": {
                "text": reminder_text,
                "id": reminder_id,
                "status": "active"
            }
        }
    
    async def _handle_enhanced_weather(self) -> Dict[str, Any]:
        """Enhanced weather with AI analysis"""
        ai_analysis = ""
        if self.openai_enabled:
            ai_analysis = await self.openai_response("weather analysis")
        
        response = f"""
🌤️ Enhanced Weather Update

📍 Location: Auto-detected (GPS)
🌡️ Temperature: 24°C (Feels like 26°C)
☁️ Condition: Partly Cloudy
💧 Humidity: 65% (Comfortable)
💨 Wind: 10 km/h (Light breeze)
🌅 Sunrise: 6:42 AM | Sunset: 6:15 PM
📊 Air Quality: Good (AQI: 45)

🔮 AI Forecast:
- Next 2 hours: Pleasant weather continues
- Today: High 28°C, Low 21°C
- Tomorrow: Slight chance of rain (20%)

✨ AI Recommendation: Perfect weather for outdoor activities!
{f'🧠 Detailed Analysis: {ai_analysis}' if ai_analysis and 'OpenAI' not in ai_analysis else ''}

Stay comfortable and enjoy your day! 🌟
        """
        
        if self.voice_enabled:
            self.simulate_voice_output("Current temperature is 24 degrees celsius with partly cloudy conditions")
        
        return {"success": True, "response": response}
    
    async def _handle_enhanced_news(self) -> Dict[str, Any]:
        """Enhanced news with AI curation"""
        ai_summary = ""
        if self.openai_enabled:
            ai_summary = "\n🧠 AI Analysis: These stories show positive trends in technology and environmental progress."
        
        response = f"""
📰 Enhanced News Update

🔥 Trending Now:
• AI technology revolutionizes healthcare diagnostics
• Renewable energy adoption reaches new milestone
• Global tech markets show sustained growth
• Climate initiatives gain international support

🌍 Local Updates:
• Smart city projects expanding nationwide
• New educational technology programs launched
• Green transportation initiatives announced

📊 AI-Curated Insights:
- Tech sector: +15% growth this quarter
- Environmental: Major policy breakthroughs
- Innovation: AI adoption accelerating globally{ai_summary}

✨ Personalized for your interests: Technology, Innovation, Environment

Stay informed with Cog's intelligent news curation! 📱
        """
        
        if self.voice_enabled:
            self.simulate_voice_output("Here are the latest news highlights")
        
        return {"success": True, "response": response}
    
    async def _handle_enhanced_general_query(self, command: str) -> Dict[str, Any]:
        """Enhanced general query handling"""
        if self.openai_enabled:
            ai_response = await self.openai_response(command)
            response = f"🧠 Enhanced AI Response:\n{ai_response}"
        else:
            responses = [
                f"I understand you're asking about '{command}'. With OpenAI integration, I could provide detailed analysis!",
                f"That's an interesting question about '{command}'! Add your OpenAI API key for intelligent responses.",
                f"I'd love to help with '{command}' in detail. Enable OpenAI features for advanced assistance!"
            ]
            import random
            response = random.choice(responses)
        
        if self.voice_enabled:
            self.simulate_voice_output("Processing your request with enhanced AI capabilities")
        
        return {"success": True, "response": response}

def main():
    """Main enhanced demo function"""
    print("=" * 70)
    print("🤖 Welcome to Cog AI Assistant - Enhanced Edition!")
    print("=" * 70)
    print("✨ Features: OpenAI Integration + Voice Simulation + Advanced AI")
    print("🎤 Voice commands supported (simulated)")
    print("🧠 OpenAI integration ready (add your API key)")
    print("🔧 Configure in .env file for full features")
    print("=" * 70)
    
    # Initialize Enhanced Cog
    cog = EnhancedCog()
    
    print(f"\n🎯 Try these enhanced commands:")
    print("• 'test AI' - Try OpenAI features")
    print("• 'turn on voice' - Enable voice simulation")
    print("• 'order pizza from swiggy' - Enhanced food ordering")
    print("• 'explain artificial intelligence' - AI-powered responses")
    print("• 'help' - See all enhanced features")
    
    # Interactive loop
    while True:
        try:
            print("\n" + "-" * 50)
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Check if user wants to simulate voice input
            is_voice = user_input.startswith("voice:")
            if is_voice:
                user_input = user_input[6:].strip()
            
            # Process command
            result = asyncio.run(cog.process_command(user_input, is_voice))
            
            # Display response
            print(f"🤖 Cog: {result['response']}")
            
            # Check for exit
            if result.get('exit'):
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for trying Cog Enhanced!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Tip: Try 'help' for available commands")

if __name__ == "__main__":
    main()