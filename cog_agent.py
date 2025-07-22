#!/usr/bin/env python3
"""
Cog AI Assistant - An intelligent voice and text assistant
that can perform multiple tasks including ordering food, booking tickets, shopping, etc.
"""

import os
import sys
import json
import logging
import asyncio
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv

# Import custom modules
from core.voice_processor import VoiceProcessor
from core.task_manager import TaskManager
from core.ai_brain import AIBrain
from plugins.plugin_manager import PluginManager
from ui.gui_interface import GUIInterface
from utils.config import Config
from utils.database import Database

# Load environment variables
load_dotenv()

class CogAgent:
    """
    Main Cog AI Agent class that orchestrates all components
    """
    
    def __init__(self):
        self.config = Config()
        self.logger = self._setup_logging()
        self.database = Database()
        
        # Initialize core components
        self.voice_processor = VoiceProcessor(self.config)
        self.ai_brain = AIBrain(self.config)
        self.task_manager = TaskManager(self.config, self.database)
        self.plugin_manager = PluginManager(self.config)
        
        # Initialize UI
        self.gui = GUIInterface(self)
        
        # Agent state
        self.is_running = False
        self.is_listening = False
        self.wake_word = "Hey Cog"
        
        self.logger.info("Cog AI Agent initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cog_agent.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    async def start(self):
        """Start the Cog agent"""
        self.logger.info("Starting Cog AI Agent...")
        self.is_running = True
        
        # Initialize all components
        await self._initialize_components()
        
        # Start voice listening in background
        voice_thread = threading.Thread(target=self._voice_listener_loop, daemon=True)
        voice_thread.start()
        
        # Start GUI
        gui_thread = threading.Thread(target=self.gui.run, daemon=True)
        gui_thread.start()
        
        # Welcome message
        await self.speak("Hello! I'm Cog, your AI assistant. How can I help you today?")
        
        # Main event loop
        await self._main_loop()
    
    async def _initialize_components(self):
        """Initialize all components"""
        try:
            # Load plugins
            await self.plugin_manager.load_plugins()
            
            # Initialize database
            self.database.initialize()
            
            # Test AI brain
            await self.ai_brain.initialize()
            
            self.logger.info("All components initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            raise
    
    def _voice_listener_loop(self):
        """Background voice listener loop"""
        while self.is_running:
            try:
                if self.is_listening:
                    command = self.voice_processor.listen_for_command(self.wake_word)
                    if command:
                        asyncio.run(self.process_command(command, source="voice"))
            except Exception as e:
                self.logger.error(f"Voice listener error: {e}")
    
    async def _main_loop(self):
        """Main event loop"""
        while self.is_running:
            try:
                # Check for scheduled tasks
                await self.task_manager.check_scheduled_tasks()
                
                # Process any pending tasks
                await self.task_manager.process_pending_tasks()
                
                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                await self.shutdown()
                break
            except Exception as e:
                self.logger.error(f"Main loop error: {e}")
    
    async def process_command(self, command: str, source: str = "text") -> Dict[str, Any]:
        """
        Process a user command
        
        Args:
            command: The user command
            source: Source of command (voice/text)
        
        Returns:
            Dict containing response and action taken
        """
        self.logger.info(f"Processing command from {source}: {command}")
        
        try:
            # Analyze command with AI brain
            analysis = await self.ai_brain.analyze_command(command)
            
            # Extract intent and parameters
            intent = analysis.get('intent')
            parameters = analysis.get('parameters', {})
            confidence = analysis.get('confidence', 0.0)
            
            # Log analysis
            self.logger.info(f"Command analysis - Intent: {intent}, Confidence: {confidence}")
            
            if confidence < 0.5:
                response = "I'm not sure I understood that. Could you please rephrase your request?"
                await self.speak(response)
                return {"response": response, "action": "clarification_needed"}
            
            # Route to appropriate plugin or handler
            result = await self._route_command(intent, parameters, command)
            
            # Speak response if from voice
            if source == "voice" and result.get('response'):
                await self.speak(result['response'])
            
            # Log task if needed
            if result.get('task_created'):
                task = result['task_created']
                self.database.log_task(
                    task_type=intent,
                    command=command,
                    parameters=parameters,
                    status="completed" if result.get('success') else "failed"
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            error_response = "I encountered an error processing your request. Please try again."
            if source == "voice":
                await self.speak(error_response)
            return {"response": error_response, "error": str(e)}
    
    async def _route_command(self, intent: str, parameters: Dict, command: str) -> Dict[str, Any]:
        """Route command to appropriate handler"""
        
        # Built-in intents
        if intent in ["greeting", "hello"]:
            return await self._handle_greeting()
        elif intent in ["goodbye", "exit"]:
            return await self._handle_goodbye()
        elif intent == "help":
            return await self._handle_help()
        elif intent == "status":
            return await self._handle_status()
        
        # Plugin-based intents
        plugin_result = await self.plugin_manager.execute_plugin(intent, parameters, command)
        if plugin_result:
            return plugin_result
        
        # Fallback to general AI response
        return await self._handle_general_query(command)
    
    async def _handle_greeting(self) -> Dict[str, Any]:
        """Handle greeting commands"""
        responses = [
            "Hello! I'm Cog, your AI assistant. How can I help you today?",
            "Hi there! I'm ready to assist you with any task.",
            "Hello! What would you like me to help you with?"
        ]
        import random
        response = random.choice(responses)
        return {"response": response, "action": "greeting"}
    
    async def _handle_goodbye(self) -> Dict[str, Any]:
        """Handle goodbye commands"""
        response = "Goodbye! Have a great day!"
        # Set flag to shutdown gracefully
        asyncio.create_task(self.shutdown())
        return {"response": response, "action": "goodbye"}
    
    async def _handle_help(self) -> Dict[str, Any]:
        """Handle help commands"""
        help_text = """
I'm Cog, your AI assistant. Here's what I can help you with:

🍕 Food Delivery: Order food from various apps
🎬 Movie Tickets: Book tickets on BookMyShow
🛒 Shopping: Order items from Amazon and other platforms
📅 Scheduling: Set reminders and appointments
🌤️ Weather: Get weather information
📰 News: Get latest news updates
🔍 Search: Search for information
💬 Chat: Have a conversation

Try saying things like:
- "Order pizza from Swiggy"
- "Book a movie ticket for Avengers"
- "Buy a red dress from Amazon"
- "Set a reminder for 3 PM"
- "What's the weather like?"

For a full list of capabilities, visit the settings menu.
        """
        return {"response": help_text, "action": "help"}
    
    async def _handle_status(self) -> Dict[str, Any]:
        """Handle status inquiry"""
        active_tasks = await self.task_manager.get_active_tasks()
        plugin_count = len(self.plugin_manager.loaded_plugins)
        
        status = f"""
Cog Status:
✅ System: Online
🔌 Plugins: {plugin_count} loaded
📋 Active Tasks: {len(active_tasks)}
🎤 Voice: {'Enabled' if self.is_listening else 'Disabled'}
        """
        return {"response": status, "action": "status"}
    
    async def _handle_general_query(self, command: str) -> Dict[str, Any]:
        """Handle general queries using AI"""
        try:
            response = await self.ai_brain.generate_response(command)
            return {"response": response, "action": "general_query"}
        except Exception as e:
            self.logger.error(f"Error generating AI response: {e}")
            return {
                "response": "I'm having trouble processing that request right now.",
                "error": str(e)
            }
    
    async def speak(self, text: str):
        """Convert text to speech"""
        try:
            await self.voice_processor.speak(text)
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {e}")
    
    def toggle_listening(self):
        """Toggle voice listening on/off"""
        self.is_listening = not self.is_listening
        status = "enabled" if self.is_listening else "disabled"
        self.logger.info(f"Voice listening {status}")
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        self.logger.info("Shutting down Cog AI Agent...")
        self.is_running = False
        
        # Close database connections
        self.database.close()
        
        # Save any pending tasks
        await self.task_manager.save_pending_tasks()
        
        self.logger.info("Cog AI Agent shutdown complete")

def main():
    """Main entry point"""
    try:
        # Create and run the agent
        agent = CogAgent()
        asyncio.run(agent.start())
    except KeyboardInterrupt:
        print("\nShutting down Cog...")
    except Exception as e:
        print(f"Error starting Cog: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()