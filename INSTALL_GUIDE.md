# 🔧 Cog AI Assistant - Installation Guide

## 🎯 Complete Setup for OpenAI + Voice Features

### 📋 **Prerequisites**
- Python 3.7 or higher
- pip package manager
- Internet connection
- Microphone (for voice features)

---

## 🔑 **Step 1: OpenAI API Key Setup**

### Get Your API Key:
1. Visit [OpenAI](https://openai.com/)
2. Sign up or log in to your account
3. Go to [API Keys page](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy your API key (starts with `sk-`)

### Configure in Cog:
```bash
# Edit the .env file
nano .env

# Add your API key:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

---

## 🎤 **Step 2: Voice Features Installation**

### Option A: Using pip (Recommended)
```bash
# Create virtual environment (recommended)
python3 -m venv cog_env
source cog_env/bin/activate  # On Windows: cog_env\Scripts\activate

# Install voice dependencies
pip install speech-recognition pyttsx3 pyaudio
```

### Option B: System Package Manager
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pyaudio python3-pip
pip3 install speech-recognition pyttsx3

# macOS (with Homebrew)
brew install portaudio
pip3 install pyaudio speech-recognition pyttsx3

# Windows
# Download and install Python from python.org
# Then run: pip install pyaudio speech-recognition pyttsx3
```

### Option C: Handle PyAudio Issues
If PyAudio installation fails:

```bash
# Ubuntu/Debian
sudo apt install python3-dev portaudio19-dev
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

---

## 🚀 **Step 3: Full Installation**

### Install All Dependencies:
```bash
# Clone or download Cog
git clone <repository-url>
cd cog-ai-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# If errors occur, install individually:
pip install openai speech-recognition pyttsx3
pip install tkinter  # Usually comes with Python
pip install selenium beautifulsoup4 requests
pip install pandas numpy asyncio
```

### Configure Environment:
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

Add your keys:
```env
# Required for AI features
OPENAI_API_KEY=sk-your-openai-key-here

# Voice configuration
VOICE_ENABLED=true
WAKE_WORD=Hey Cog
VOICE_RATE=180
VOICE_VOLUME=0.8

# Optional: Other API keys
WEATHER_API_KEY=your_weather_key
NEWS_API_KEY=your_news_key
```

---

## 🎮 **Step 4: Test Your Installation**

### Quick Test:
```bash
# Test basic functionality
python3 demo_cog.py

# Test enhanced features
python3 cog_enhanced.py

# Test full version (with GUI)
python3 cog_agent.py
```

### Verify Features:
```bash
# In Cog, try these commands:
test AI          # Test OpenAI integration
turn on voice    # Test voice features
help            # See all available features
```

---

## ⚙️ **Step 5: Advanced Configuration**

### Voice Settings:
```python
# In .env file:
VOICE_ENABLED=true
WAKE_WORD=Hey Cog           # Customize wake word
VOICE_RATE=180              # Speech speed (100-300)
VOICE_VOLUME=0.8            # Volume (0.0-1.0)
```

### OpenAI Settings:
```python
# Advanced AI configuration:
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
OPENAI_MAX_TOKENS=150       # Response length
OPENAI_TEMPERATURE=0.7      # Creativity (0.0-1.0)
```

---

## 🛠️ **Troubleshooting**

### Common Issues:

#### 1. **PyAudio Installation Fails**
```bash
# Solution 1: Install system dependencies
sudo apt install python3-dev portaudio19-dev  # Ubuntu/Debian
brew install portaudio                         # macOS

# Solution 2: Use conda
conda install pyaudio

# Solution 3: Use pre-compiled wheel
pip install pipwin && pipwin install pyaudio  # Windows
```

#### 2. **OpenAI API Errors**
```bash
# Check API key format (should start with sk-)
# Verify account has credits
# Test with: python3 -c "import openai; print('OpenAI installed')"
```

#### 3. **Voice Recognition Not Working**
```bash
# Check microphone permissions
# Test microphone: python3 -c "import speech_recognition as sr; print('Mic test OK')"
# Adjust microphone settings in system preferences
```

#### 4. **GUI Not Loading**
```bash
# Install tkinter:
sudo apt install python3-tk  # Ubuntu/Debian
# On macOS/Windows, tkinter comes with Python
```

#### 5. **Import Errors**
```bash
# Verify virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 🎉 **Step 6: Verify Complete Setup**

### Test All Features:
```bash
python3 cog_enhanced.py
```

Try these commands in sequence:
1. `help` - See all features
2. `test AI` - Verify OpenAI works
3. `turn on voice` - Enable voice features
4. `voice: hey cog order pizza` - Test voice input
5. `order pizza from swiggy` - Test enhanced ordering
6. `buy headphones from amazon` - Test shopping
7. `what's the weather?` - Test AI-enhanced responses

### Expected Results:
- ✅ OpenAI responses work with your API key
- ✅ Voice simulation shows input/output
- ✅ All ordering/booking features functional
- ✅ Enhanced AI suggestions appear
- ✅ No import or dependency errors

---

## 📱 **Usage Examples**

### Voice Commands:
```bash
# Prefix with "voice:" to simulate voice input
voice: hey cog order pizza from swiggy
voice: hey cog book movie tickets for avengers
voice: hey cog what's the weather like today
```

### AI-Enhanced Commands:
```bash
explain artificial intelligence
tell me about quantum computing
test AI features
get weather analysis
```

### Regular Commands:
```bash
order 2 burgers from zomato
buy red dress from amazon
remind me to call mom at 5 PM
latest news updates
```

---

## 🔄 **Updates and Maintenance**

### Keep Cog Updated:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update OpenAI library
pip install --upgrade openai

# Check for Cog updates
git pull origin main  # If using git
```

### Monitor Usage:
- Check OpenAI usage at [platform.openai.com](https://platform.openai.com/usage)
- Monitor API costs and set usage limits
- Review voice recognition accuracy

---

## 💡 **Pro Tips**

1. **Save API Costs**: Use pattern matching for simple queries, OpenAI for complex ones
2. **Voice Quality**: Use a good microphone for better recognition
3. **Customization**: Modify intent patterns in `cog_enhanced.py` for better recognition
4. **Performance**: Use virtual environment to avoid conflicts
5. **Security**: Never share your API keys publicly

---

## 🆘 **Still Having Issues?**

1. Check the main [README.md](README.md) for general information
2. Try the basic demo first: `python3 demo_cog.py`
3. Use the launcher: `python3 launch_cog.py`
4. Check logs: `cog_agent.log`
5. Verify Python version: `python3 --version` (should be 3.7+)

---

**🎊 Congratulations! Cog is now fully configured with OpenAI and voice features!**

*Ready to experience the future of AI assistants!* 🤖✨