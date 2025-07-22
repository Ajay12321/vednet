# 🚀 Cog AI Assistant - Quick Start Guide

## 🎯 Try the Demo (No Setup Required!)

The fastest way to experience Cog is with the demo version:

```bash
python3 demo_cog.py
```

### Demo Commands to Try:
- `help` - See all available commands
- `order pizza from swiggy` - Order food
- `book movie tickets for avengers` - Book movie tickets  
- `buy a red dress from amazon` - Shop online
- `remind me to call mom` - Set reminders
- `what's the weather?` - Get weather info
- `latest news` - Get news updates
- `exit` - Quit the demo

## 🏃‍♂️ Quick Installation

### Option 1: Simple Demo (Recommended for first try)
```bash
# Clone or download the project
git clone <repo-url>
cd cog-ai-assistant

# Run the demo (works immediately)
python3 demo_cog.py
```

### Option 2: Full Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (optional)
cp .env.example .env
# Edit .env file to add your OpenAI API key

# Run the full version
python3 cog_agent.py
```

### Option 3: Auto-installer
```bash
# Let the launcher handle everything
python3 launch_cog.py
```

## 🎤 Voice Features

1. Click the microphone button in the GUI
2. Say "Hey Cog" to activate
3. Speak your command naturally
4. Cog will respond with voice and text

## 🔧 Configuration

### Environment Variables
Add to `.env` file:
```env
OPENAI_API_KEY=your_key_here  # For advanced AI features
VOICE_ENABLED=true            # Enable voice features
WAKE_WORD=Hey Cog            # Customize wake word
```

### Voice Settings
- Adjust speech rate and volume in GUI settings
- Select different voices
- Customize wake word

## 🌟 Example Scenarios

### 🍕 Ordering Food
```
You: "I'm hungry, order some pizza"
Cog: "Ordering large pizza from Swiggy. Order ID: SWIGGY_A1B2C3D4. 
      Estimated delivery: 30-45 minutes. Total: ₹299"
```

### 🎬 Movie Night
```
You: "Book tickets for the new Marvel movie"
Cog: "Found Avengers: Endgame at PVR Cinemas. Booked 2 tickets for 
      7:00 PM. Booking ID: BMS_X1Y2Z3A4. Total: ₹500"
```

### 🛒 Shopping
```
You: "Buy a blue dress under ₹2000"
Cog: "Found Women's Casual Dress in blue for ₹1,299 on Amazon. 
      4.2-star rating. Added to cart. Free delivery tomorrow!"
```

## ❓ Troubleshooting

### Common Issues

**Voice not working:**
- Install PyAudio: `pip install pyaudio`
- Check microphone permissions
- Try running as administrator (Windows)

**Import errors:**
- Run: `pip install -r requirements.txt`
- Use Python 3.7 or higher
- Try the demo version first: `python3 demo_cog.py`

**No response:**
- Check internet connection
- Verify OpenAI API key (for advanced features)
- Try simpler commands first

### Still Having Issues?
1. Try the demo version: `python3 demo_cog.py`
2. Check the logs: `cog_agent.log`
3. Run with auto-installer: `python3 launch_cog.py`

## 🎉 What's Next?

After trying the demo:
1. Set up OpenAI API key for smarter responses
2. Configure real platform APIs for actual ordering
3. Customize voice settings
4. Explore the plugin system
5. Build your own plugins

## 📞 Support

- Read the full [README.md](README.md)
- Check troubleshooting section
- Review the code examples
- Ask questions in issues

---

**🤖 Welcome to the future of personal AI assistants!**

*Try the demo now: `python3 demo_cog.py`*