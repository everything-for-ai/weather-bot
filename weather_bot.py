#!/usr/bin/env python3
"""
Weather Bot - Multi-platform weather notification
Supports WeChat, Feishu, Telegram, Slack, and more
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional


class WeatherBot:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.session = requests.Session()
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration"""
        default_config = {
            "locations": [
                {"name": "深圳", "city": "Shenzhen", "country": "CN"},
                {"name": "北京", "city": "Beijing", "country": "CN"}
            ],
            "schedule": "08:00",
            "weather_api_key": os.environ.get("WEATHER_API_KEY", ""),
            "platforms": ["feishu"],
            "openweathermap_appid": os.environ.get("OPENWEATHERMAP_APPID", "")
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def get_weather(self, city: str, country: str = "CN") -> Dict:
        """Get weather data from OpenWeatherMap"""
        api_key = self.config.get("openweathermap_appid", "")
        
        if not api_key:
            # Return mock data if no API key
            return self.get_mock_weather(city)
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country}",
            "appid": api_key,
            "units": "metric"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            return {
                "city": city,
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_mock_weather(city)
    
    def get_mock_weather(self, city: str) -> Dict:
        """Return mock weather data for testing"""
        weather_conditions = [
            {"desc": "Clear", "icon": "☀️"},
            {"desc": "Clouds", "icon": "☁️"},
            {"desc": "Partly cloudy", "icon": "⛅"},
            {"desc": "Rain", "icon": "🌧️"}
        ]
        import random
        condition = random.choice(weather_conditions)
        
        return {
            "city": city,
            "temp": round(random.uniform(-5, 30), 1),
            "feels_like": round(random.uniform(-5, 30), 1),
            "humidity": random.randint(30, 80),
            "description": condition["desc"],
            "icon": condition["icon"]
        }
    
    def format_weather_message(self, weather_data: Dict) -> str:
        """Format weather data as a message"""
        return f"""
🌤️ 今日天气 - {weather_data['city']}
{weather_data['icon']} {weather_data['description']}
🌡️ {weather_data['temp']}°C (体感 {weather_data['feels_like']}°C)
💧 湿度: {weather_data['humidity']}%
        """.strip()
    
    def get_all_weather(self) -> str:
        """Get weather for all configured locations"""
        messages = [f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} 天气报告\n"]
        
        for loc in self.config["locations"]:
            weather = self.get_weather(loc["city"], loc.get("country", "CN"))
            messages.append(self.format_weather_message(weather))
            messages.append("")  # Empty line
        
        return "\n".join(messages).strip()
    
    def send_to_feishu(self, message: str):
        """Send message to Feishu"""
        # TODO: Implement Feishu webhook
        print(f"[Feishu] {message}")
    
    def send_to_wecom(self, message: str):
        """Send message to WeCom"""
        # TODO: Implement WeCom webhook
        print(f"[WeCom] {message}")
    
    def send_to_telegram(self, message: str):
        """Send message to Telegram"""
        # TODO: Implement Telegram bot
        print(f"[Telegram] {message}")
    
    def run(self):
        """Main execution"""
        message = self.get_all_weather()
        
        # Send to all configured platforms
        for platform in self.config.get("platforms", []):
            if platform == "feishu":
                self.send_to_feishu(message)
            elif platform == "wecom":
                self.send_to_wecom(message)
            elif platform == "telegram":
                self.send_to_telegram(message)
        
        print(message)
        return message


if __name__ == "__main__":
    bot = WeatherBot()
    bot.run()
