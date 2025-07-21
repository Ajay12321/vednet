# VedNet - Comprehensive Task Management System

🌟 **Your personal AI assistant for daily life management** 🌟

VedNet is a powerful, comprehensive task management system that handles all your daily activities including food ordering, dress recommendations, stock predictions, weather updates, calendar management, shopping assistance, fitness tracking, and personal finance management.

## 🚀 Features

### Core Capabilities
- **🍕 Food Ordering & Meal Planning** - Restaurant recommendations, meal planning, nutrition tracking
- **👗 Dress & Style Recommendations** - Weather-appropriate outfits, style advice, color coordination
- **📈 Stock Market Predictions** - Portfolio analysis, market insights, investment recommendations
- **🌤️ Weather Updates** - Current conditions, forecasts, activity planning
- **📅 Calendar Management** - Schedule optimization, meeting suggestions, time blocking
- **🛒 Shopping Assistant** - Smart lists, price comparisons, route optimization
- **💪 Fitness Tracking** - Workout plans, health metrics, goal tracking
- **💰 Finance Management** - Budget analysis, expense tracking, financial goals

### Smart Automation
- **Automated Daily Tasks** - Run all tasks with a single command
- **Intelligent Recommendations** - AI-powered suggestions based on your preferences
- **Data Persistence** - All your data is saved and tracked over time
- **Rich Console Interface** - Beautiful, colorful terminal interface
- **Comprehensive Logging** - Detailed logs for debugging and tracking

## 📋 Requirements

- Python 3.8+
- Internet connection (for real-time data when APIs are configured)
- Terminal/Command Line interface

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd vednet
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

## 🎯 Quick Start

1. **Launch VedNet:**
```bash
python main.py
```

2. **Choose from the menu:**
   - `1` - Food Ordering & Meal Planning
   - `2` - Dress & Style Recommendations
   - `3` - Stock Market Analysis
   - `4` - Weather Updates
   - `5` - Calendar Management
   - `6` - Shopping Assistant
   - `7` - Fitness Tracking
   - `8` - Finance Management
   - `9` - **Smart Automation (Run All Tasks)**
   - `10` - View Task Status

3. **Smart Automation** (Recommended):
   Select option `9` to run all daily tasks automatically and get a comprehensive overview of your day.

## 📁 Project Structure

```
vednet/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── tasks/                  # Task modules
│   ├── food_ordering.py    # Food & meal management
│   ├── dress_recommendations.py # Style & outfit suggestions
│   ├── stock_predictions.py    # Market analysis
│   ├── weather_task.py     # Weather updates
│   ├── calendar_task.py    # Calendar management
│   ├── shopping_task.py    # Shopping assistance
│   ├── fitness_task.py     # Fitness tracking
│   └── finance_task.py     # Finance management
├── utils/                  # Utility modules
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging utilities
├── data/                  # Data storage (auto-created)
└── logs/                  # Application logs (auto-created)
```

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file for API keys:

```bash
OPENWEATHER_API_KEY=your_weather_api_key
FOOD_DELIVERY_API_KEY=your_food_api_key
OPENAI_API_KEY=your_openai_key
ALPHA_VANTAGE_API_KEY=your_stock_api_key
```

### User Preferences
The system creates a `data/config.json` file with your preferences:

```json
{
  "user_preferences": {
    "location": "New York, NY",
    "cuisine_preferences": ["Italian", "Indian", "Mexican"],
    "dietary_restrictions": [],
    "budget_range": {"min": 10, "max": 50},
    "style_preferences": ["casual", "business", "formal"],
    "fitness_goals": {"daily_steps": 10000, "weekly_workouts": 3}
  }
}
```

## 🎮 Usage Examples

### Daily Automation
```bash
# Run all daily tasks automatically
python main.py
# Select option 9 for Smart Automation
```

### Individual Tasks
```bash
# Food recommendations and meal planning
python main.py
# Select option 1

# Get outfit suggestions based on weather
python main.py
# Select option 2

# Analyze your stock portfolio
python main.py
# Select option 3
```

## 📊 Data Management

### Automatic Data Storage
- **Food Data**: `data/meal_plan_YYYYMMDD.json`, `data/food_orders.json`
- **Style Data**: `data/outfit_plan_YYYYMMDD.json`
- **Stock Data**: `data/stock_analysis_YYYYMMDD.json`
- **Weather Data**: `data/weather_YYYYMMDD.json`
- **Calendar Data**: `data/calendar_events.json`, `data/calendar_summary_YYYYMMDD.json`
- **Shopping Data**: `data/shopping_lists.json`, `data/shopping_summary_YYYYMMDD.json`
- **Fitness Data**: `data/fitness_data.json`, `data/fitness_summary_YYYYMMDD.json`
- **Finance Data**: `data/financial_data.json`, `data/finance_summary_YYYYMMDD.json`

### Logs
- Daily logs stored in `logs/vednet_YYYYMMDD.log`
- Color-coded console output for easy debugging

## 🔧 Customization

### Adding New Tasks
1. Create a new task manager in `tasks/`
2. Implement the `execute()` method
3. Add to main application in `main.py`

### Modifying Preferences
Edit `data/config.json` or use the configuration management system.

## 🚀 Advanced Features

### Stock Market Analysis
- Real-time stock data (when API configured)
- Technical analysis with moving averages and RSI
- Portfolio performance tracking
- Investment recommendations

### Weather Integration
- Current conditions and forecasts
- Outfit suggestions based on weather
- Activity planning recommendations

### Fitness Tracking
- Workout recommendations
- Goal progress tracking
- Achievement system
- Nutrition suggestions

### Financial Management
- Budget analysis and tracking
- Spending pattern analysis
- Financial goal monitoring
- Investment portfolio overview

## 🛡️ Privacy & Security

- All data stored locally on your machine
- No data transmitted unless you configure external APIs
- Encrypted configuration for sensitive information
- Regular data backups recommended

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🎉 Getting Started

Ready to transform your daily routine? Run VedNet now:

```bash
python main.py
```

Select option `9` for the full experience and let VedNet handle all your daily tasks automatically!

---

**Happy Task Managing!** 🌟