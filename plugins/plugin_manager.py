"""
Plugin Manager for Cog AI Agent
Manages loading and execution of plugins for various services
"""

import asyncio
import logging
import importlib
import os
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = ""
        self.supported_intents = []
    
    @abstractmethod
    async def execute(self, intent: str, parameters: Dict[str, Any], command: str) -> Dict[str, Any]:
        """Execute the plugin functionality"""
        pass
    
    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        """Check if plugin can handle the given intent"""
        pass
    
    async def initialize(self) -> bool:
        """Initialize the plugin (optional override)"""
        return True
    
    async def cleanup(self):
        """Cleanup plugin resources (optional override)"""
        pass

class PluginManager:
    """
    Manages all plugins for the Cog AI Agent
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.loaded_plugins: Dict[str, BasePlugin] = {}
        self.plugin_directory = "plugins"
        
        self.logger.info("Plugin Manager initialized")
    
    async def load_plugins(self):
        """Load all available plugins"""
        try:
            # Load built-in plugins
            await self._load_builtin_plugins()
            
            # Load custom plugins from directory
            await self._load_directory_plugins()
            
            self.logger.info(f"Loaded {len(self.loaded_plugins)} plugins")
            
        except Exception as e:
            self.logger.error(f"Error loading plugins: {e}")
    
    async def _load_builtin_plugins(self):
        """Load built-in plugins"""
        from plugins.food_ordering_plugin import FoodOrderingPlugin
        from plugins.movie_booking_plugin import MovieBookingPlugin
        from plugins.shopping_plugin import ShoppingPlugin
        from plugins.reminder_plugin import ReminderPlugin
        from plugins.weather_plugin import WeatherPlugin
        from plugins.news_plugin import NewsPlugin
        from plugins.search_plugin import SearchPlugin
        
        builtin_plugins = [
            FoodOrderingPlugin,
            MovieBookingPlugin,
            ShoppingPlugin,
            ReminderPlugin,
            WeatherPlugin,
            NewsPlugin,
            SearchPlugin
        ]
        
        for plugin_class in builtin_plugins:
            try:
                plugin = plugin_class(self.config)
                if await plugin.initialize():
                    self.loaded_plugins[plugin.name] = plugin
                    self.logger.info(f"Loaded plugin: {plugin.name}")
                else:
                    self.logger.warning(f"Failed to initialize plugin: {plugin.name}")
            except Exception as e:
                self.logger.error(f"Error loading plugin {plugin_class.__name__}: {e}")
    
    async def _load_directory_plugins(self):
        """Load plugins from the plugins directory"""
        if not os.path.exists(self.plugin_directory):
            return
        
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('_plugin.py') and not filename.startswith('__'):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    module = importlib.import_module(f"plugins.{module_name}")
                    
                    # Look for plugin classes
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, BasePlugin) and 
                            attr != BasePlugin):
                            
                            plugin = attr(self.config)
                            if await plugin.initialize():
                                self.loaded_plugins[plugin.name] = plugin
                                self.logger.info(f"Loaded custom plugin: {plugin.name}")
                            
                except Exception as e:
                    self.logger.error(f"Error loading custom plugin {module_name}: {e}")
    
    async def execute_plugin(self, intent: str, parameters: Dict[str, Any], command: str) -> Optional[Dict[str, Any]]:
        """
        Execute a plugin based on intent
        
        Args:
            intent: The intent to handle
            parameters: Parameters extracted from command
            command: Original command text
            
        Returns:
            Plugin execution result or None if no plugin can handle
        """
        for plugin_name, plugin in self.loaded_plugins.items():
            try:
                if plugin.can_handle(intent):
                    self.logger.info(f"Executing plugin {plugin_name} for intent: {intent}")
                    result = await plugin.execute(intent, parameters, command)
                    result['plugin_used'] = plugin_name
                    return result
            except Exception as e:
                self.logger.error(f"Error executing plugin {plugin_name}: {e}")
                continue
        
        self.logger.debug(f"No plugin found to handle intent: {intent}")
        return None
    
    def get_plugin_info(self) -> List[Dict[str, Any]]:
        """Get information about loaded plugins"""
        info = []
        for plugin in self.loaded_plugins.values():
            info.append({
                'name': plugin.name,
                'version': plugin.version,
                'description': plugin.description,
                'supported_intents': plugin.supported_intents
            })
        return info
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin"""
        try:
            if plugin_name in self.loaded_plugins:
                await self.loaded_plugins[plugin_name].cleanup()
                del self.loaded_plugins[plugin_name]
            
            # Reload the plugin
            await self.load_plugins()
            
            if plugin_name in self.loaded_plugins:
                self.logger.info(f"Plugin {plugin_name} reloaded successfully")
                return True
            else:
                self.logger.error(f"Failed to reload plugin {plugin_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error reloading plugin {plugin_name}: {e}")
            return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin"""
        try:
            if plugin_name in self.loaded_plugins:
                await self.loaded_plugins[plugin_name].cleanup()
                del self.loaded_plugins[plugin_name]
                self.logger.info(f"Plugin {plugin_name} unloaded")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    async def cleanup_all_plugins(self):
        """Cleanup all loaded plugins"""
        for plugin in self.loaded_plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up plugin {plugin.name}: {e}")
        
        self.loaded_plugins.clear()
        self.logger.info("All plugins cleaned up")
    
    def get_plugins_for_intent(self, intent: str) -> List[str]:
        """Get list of plugins that can handle a specific intent"""
        capable_plugins = []
        for plugin_name, plugin in self.loaded_plugins.items():
            if plugin.can_handle(intent):
                capable_plugins.append(plugin_name)
        return capable_plugins