# Cog AI Assistant 🤖

**Cog** is a comprehensive AI assistant that can handle multiple tasks through voice and text commands, similar to Siri but with enhanced capabilities for ordering food, booking movie tickets, shopping, and much more.

## 🌟 Features

### 🍕 **Food Ordering**
- Order food from Swiggy, Zomato, UberEats
- Specify cuisine, quantity, and preferences
- Track order status

### 🎬 **Movie Booking**
- Book tickets on BookMyShow and other platforms
- Find movies, theaters, and showtimes
- Select seats and complete bookings

### 🛒 **Shopping**
- Shop on Amazon, Flipkart, Myntra
- Search for products with specific criteria
- Compare prices across platforms

### 📅 **Reminders & Scheduling**
- Set reminders with natural language
- Schedule tasks for specific times
- Get notifications

### 🌤️ **Weather & News**
- Get current weather information
- Latest news updates
- Location-based information

### 🎤 **Voice Assistant**
- Wake word activation ("Hey Cog")
- Speech-to-text recognition
- Text-to-speech responses
- Continuous listening mode

### 💬 **Natural Language Processing**
- Advanced intent recognition
- Context-aware conversations
- Multi-modal interaction (voice + text)

### 🔌 **Plugin Architecture**
- Extensible plugin system
- Easy to add new services
- Modular design

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Microphone (for voice features)
- Internet connection

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cog-ai-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
cp .env.example .env
```
Edit the `.env` file and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run Cog
```bash
python cog_agent.py
```

## 🎯 Usage

### Text Commands
Type commands in the GUI or use the command line interface:

```
🍕 Food Ordering:
- "Order pizza from Swiggy"
- "Get me biryani from Zomato"
- "I want Chinese food"

🎬 Movie Booking:
- "Book tickets for Avengers"
- "Movie ticket for tonight"
- "Show me movies at PVR"

🛒 Shopping:
- "Buy a red dress from Amazon"
- "Order iPhone from Flipkart"
- "Search for running shoes"

📅 Reminders:
- "Remind me to call mom at 3 PM"
- "Set reminder for tomorrow"
- "Schedule meeting for next week"

🌤️ Information:
- "What's the weather?"
- "Get latest news"
- "Search for Python tutorials"
```

### Voice Commands
1. Enable voice mode by clicking the microphone button
2. Say "Hey Cog" to activate
3. Speak your command naturally
4. Cog will respond with voice and text

## 🔧 Configuration

### Voice Settings
- Wake word customization
- Speech rate adjustment
- Volume control
- Voice selection

### API Integration
Configure API keys in `.env` file for enhanced functionality:
- OpenAI for advanced AI responses
- Weather APIs for real-time data
- Platform-specific APIs for actual ordering

### Database
Cog uses SQLite to store:
- Task history
- User preferences
- Command logs
- Plugin configurations

## 🏗️ Architecture

```
cog-ai-assistant/
├── cog_agent.py              # Main application
├── core/
│   ├── voice_processor.py    # Speech recognition & TTS
│   ├── ai_brain.py          # NLP & intent recognition
│   └── task_manager.py      # Task execution & scheduling
├── plugins/
│   ├── plugin_manager.py    # Plugin system
│   ├── food_ordering_plugin.py
│   ├── movie_booking_plugin.py
│   ├── shopping_plugin.py
│   └── ...
├── ui/
│   └── gui_interface.py     # Graphical interface
├── utils/
│   ├── config.py           # Configuration management
│   └── database.py         # Database operations
└── requirements.txt
```

## 🔌 Plugin Development

Create custom plugins by extending the `BasePlugin` class:

```python
from plugins.plugin_manager import BasePlugin

class MyCustomPlugin(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.name = "MyCustomPlugin"
        self.supported_intents = ["my_intent"]
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.supported_intents
    
    async def execute(self, intent: str, parameters: Dict[str, Any], command: str) -> Dict[str, Any]:
        # Your plugin logic here
        return {"success": True, "message": "Custom action completed"}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Troubleshooting

### Common Issues

**Voice not working:**
- Check microphone permissions
- Install pyaudio: `pip install pyaudio`
- Verify microphone hardware

**API errors:**
- Ensure OpenAI API key is valid
- Check internet connection
- Verify API key format

**Plugin errors:**
- Check plugin dependencies
- Verify plugin configuration
- Review logs for detailed errors

### Logs
Check `cog_agent.log` for detailed error information.

## 🎉 Example Scenarios

### Scenario 1: Planning a Movie Night
```
You: "Hey Cog, book tickets for the new Marvel movie tonight"
Cog: "I found Avengers: Endgame playing at PVR Cinemas. Booking 2 tickets for 7:00 PM show. Total cost: ₹500. Booking confirmed with ID: BMS_A1B2C3D4"
```

### Scenario 2: Ordering Dinner
```
You: "I'm hungry, order some pizza"
Cog: "Ordering large pizza from Domino's. Estimated delivery: 30-45 minutes. Order total: ₹349. Order ID: SWIGGY_XYZ123"
```

### Scenario 3: Shopping Assistant
```
You: "Buy a blue dress for under ₹2000"
Cog: "Found Women's Casual Dress in blue for ₹1,299 on Amazon. 4.2-star rating. Added to cart. Free delivery tomorrow."
```

## 🌟 Roadmap

- [ ] Integration with real APIs (Swiggy, BookMyShow, etc.)
- [ ] Calendar integration
- [ ] Smart home controls
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Advanced conversation memory
- [ ] Custom voice training
- [ ] Webhook integrations

## 📞 Support

For support, please:
1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with detailed information
4. Contact the development team

---

**Made with ❤️ by the Cog Development Team**

*Cog - Your intelligent assistant for everything!*