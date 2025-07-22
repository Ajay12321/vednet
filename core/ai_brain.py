"""
AI Brain Module for Cog AI Agent
Handles natural language understanding, intent recognition, and AI-powered responses
"""

import asyncio
import logging
import json
import re
from typing import Dict, List, Any, Optional
import openai
from datetime import datetime

class AIBrain:
    """
    AI Brain that processes natural language and determines intent
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Set OpenAI API key
        openai.api_key = config.get('openai_api_key')
        
        # Intent patterns for quick matching
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
            'status': [
                r'\b(status|how are you|what\'s up)\b'
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
            ],
            'search': [
                r'\bsearch for\b',
                r'\blook up\b',
                r'\bfind.*information\b'
            ]
        }
        
        self.logger.info("AI Brain initialized")
    
    async def initialize(self):
        """Initialize the AI brain and test connections"""
        try:
            # Test OpenAI connection
            if openai.api_key:
                # Simple test to verify API key works
                test_response = await self._make_openai_request(
                    "Test connection", max_tokens=5
                )
                self.logger.info("OpenAI connection verified")
            else:
                self.logger.warning("No OpenAI API key provided - using pattern matching only")
        except Exception as e:
            self.logger.error(f"Error initializing AI brain: {e}")
    
    async def analyze_command(self, command: str) -> Dict[str, Any]:
        """
        Analyze a command to extract intent and parameters
        
        Args:
            command: User command text
            
        Returns:
            Dict with intent, parameters, and confidence
        """
        command_lower = command.lower().strip()
        
        # First try pattern matching for quick responses
        pattern_result = self._pattern_match_intent(command_lower)
        if pattern_result['confidence'] > 0.7:
            return pattern_result
        
        # If pattern matching isn't confident, use AI
        if openai.api_key:
            try:
                ai_result = await self._ai_analyze_command(command)
                return ai_result
            except Exception as e:
                self.logger.error(f"Error in AI analysis: {e}")
                # Fallback to pattern matching
                return pattern_result
        
        return pattern_result
    
    def _pattern_match_intent(self, command: str) -> Dict[str, Any]:
        """
        Use pattern matching to determine intent
        
        Args:
            command: Lowercased command text
            
        Returns:
            Dict with intent, parameters, and confidence
        """
        best_intent = "general_query"
        best_confidence = 0.0
        parameters = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    confidence = 0.8  # High confidence for pattern matches
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
        
        # Extract basic parameters based on intent
        if best_intent == 'food_order':
            parameters = self._extract_food_parameters(command)
        elif best_intent == 'movie_booking':
            parameters = self._extract_movie_parameters(command)
        elif best_intent == 'shopping':
            parameters = self._extract_shopping_parameters(command)
        elif best_intent == 'reminder':
            parameters = self._extract_reminder_parameters(command)
        
        return {
            'intent': best_intent,
            'parameters': parameters,
            'confidence': best_confidence,
            'method': 'pattern_matching'
        }
    
    def _extract_food_parameters(self, command: str) -> Dict[str, Any]:
        """Extract food ordering parameters"""
        parameters = {}
        
        # Extract food type
        food_items = ['pizza', 'burger', 'biryani', 'chicken', 'chinese', 'indian', 'pasta']
        for item in food_items:
            if item in command:
                parameters['food_type'] = item
                break
        
        # Extract platform
        platforms = ['swiggy', 'zomato', 'ubereats', 'doordash']
        for platform in platforms:
            if platform in command:
                parameters['platform'] = platform
                break
        
        # Extract quantity
        quantity_match = re.search(r'\b(\d+)\b', command)
        if quantity_match:
            parameters['quantity'] = int(quantity_match.group(1))
        
        return parameters
    
    def _extract_movie_parameters(self, command: str) -> Dict[str, Any]:
        """Extract movie booking parameters"""
        parameters = {}
        
        # Extract movie name (simple approach)
        movie_indicators = ['for', 'movie', 'film']
        for indicator in movie_indicators:
            if indicator in command:
                parts = command.split(indicator)
                if len(parts) > 1:
                    potential_movie = parts[-1].strip()
                    parameters['movie_name'] = potential_movie
                    break
        
        # Extract date/time
        time_patterns = [
            r'\b(today|tomorrow|tonight)\b',
            r'\b(\d{1,2})\s*(pm|am)\b',
            r'\b(\d{1,2})/(\d{1,2})\b'
        ]
        for pattern in time_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                parameters['time'] = match.group(0)
                break
        
        return parameters
    
    def _extract_shopping_parameters(self, command: str) -> Dict[str, Any]:
        """Extract shopping parameters"""
        parameters = {}
        
        # Extract item type
        items = ['dress', 'shirt', 'shoes', 'book', 'phone', 'laptop', 'clothes']
        for item in items:
            if item in command:
                parameters['item_type'] = item
                break
        
        # Extract color
        colors = ['red', 'blue', 'black', 'white', 'green', 'yellow', 'pink']
        for color in colors:
            if color in command:
                parameters['color'] = color
                break
        
        # Extract platform
        platforms = ['amazon', 'flipkart', 'myntra', 'ebay']
        for platform in platforms:
            if platform in command:
                parameters['platform'] = platform
                break
        
        return parameters
    
    def _extract_reminder_parameters(self, command: str) -> Dict[str, Any]:
        """Extract reminder parameters"""
        parameters = {}
        
        # Extract time
        time_patterns = [
            r'\bat\s*(\d{1,2})\s*(pm|am)\b',
            r'\bin\s*(\d+)\s*(minutes?|hours?|days?)\b',
            r'\b(today|tomorrow|next week)\b'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                parameters['time'] = match.group(0)
                break
        
        # Extract reminder text
        remind_keywords = ['remind me to', 'remind me', 'set reminder']
        for keyword in remind_keywords:
            if keyword in command:
                parts = command.split(keyword)
                if len(parts) > 1:
                    reminder_text = parts[-1].strip()
                    parameters['reminder_text'] = reminder_text
                    break
        
        return parameters
    
    async def _ai_analyze_command(self, command: str) -> Dict[str, Any]:
        """
        Use AI to analyze command intent and extract parameters
        
        Args:
            command: User command
            
        Returns:
            Dict with intent, parameters, and confidence
        """
        system_prompt = """
You are an AI assistant that analyzes user commands to determine intent and extract parameters.

Available intents:
- greeting: User greeting
- goodbye: User saying goodbye
- help: User asking for help
- status: User asking about status
- food_order: User wants to order food
- movie_booking: User wants to book movie tickets
- shopping: User wants to buy something
- reminder: User wants to set a reminder
- weather: User asking about weather
- news: User asking for news
- search: User wants to search for information
- general_query: General question or conversation

Respond with JSON in this format:
{
    "intent": "intent_name",
    "parameters": {
        "key": "value"
    },
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}
"""
        
        user_prompt = f"Analyze this command: '{command}'"
        
        try:
            response = await self._make_openai_request(
                user_prompt,
                system_message=system_prompt,
                max_tokens=200
            )
            
            # Parse JSON response
            result = json.loads(response)
            result['method'] = 'ai_analysis'
            return result
            
        except json.JSONDecodeError:
            self.logger.error("Failed to parse AI response as JSON")
            return self._pattern_match_intent(command.lower())
        except Exception as e:
            self.logger.error(f"Error in AI analysis: {e}")
            return self._pattern_match_intent(command.lower())
    
    async def generate_response(self, query: str) -> str:
        """
        Generate an AI response to a general query
        
        Args:
            query: User query
            
        Returns:
            AI-generated response
        """
        if not openai.api_key:
            return "I'm sorry, I need an OpenAI API key to answer general questions. Please configure one in the settings."
        
        try:
            system_prompt = """
You are Cog, a helpful AI assistant. You are friendly, knowledgeable, and concise.
Keep responses brief but informative. If you don't know something, say so.
"""
            
            response = await self._make_openai_request(
                query,
                system_message=system_prompt,
                max_tokens=300
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating AI response: {e}")
            return "I'm having trouble generating a response right now. Please try again later."
    
    async def _make_openai_request(self, prompt: str, system_message: str = None, max_tokens: int = 150) -> str:
        """
        Make a request to OpenAI API (simplified version that works without API key)
        
        Args:
            prompt: User prompt
            system_message: System message
            max_tokens: Maximum tokens in response
            
        Returns:
            AI response text
        """
        # For demo purposes, return a simple response if no API key
        if not openai.api_key:
            return "This feature requires an OpenAI API key. Please configure one in the settings."
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Note: This would use the OpenAI API with a valid key
            import openai as openai_client
            response = openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return "I'm having trouble with the AI service right now."
    
    def update_intent_patterns(self, intent: str, patterns: List[str]):
        """
        Update intent patterns for better recognition
        
        Args:
            intent: Intent name
            patterns: List of regex patterns
        """
        self.intent_patterns[intent] = patterns
        self.logger.info(f"Updated patterns for intent: {intent}")
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intents"""
        return list(self.intent_patterns.keys())