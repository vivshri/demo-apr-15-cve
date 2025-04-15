# app.py - Example vulnerable code
import os
import logging
import json
import requests
import urllib3

# This is vulnerable to CVE-2023-32681 because urllib3 version is < 2.0.3
# The vulnerability allows HTTP request smuggling via headers with CR or LF

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weatherapi.com/v1/current.json"
    
    def get_weather(self, city, user_headers=None):
        """
        Get weather for a city
        
        This implementation has a vulnerability because it directly passes user-provided
        headers to the requests library without sanitizing them
        """
        params = {
            'key': self.api_key,
            'q': city
        }
        
        # Vulnerable code: Directly passing user-provided headers
        # This could allow HTTP request smuggling with urllib3 < 2.0.3
        headers = {'User-Agent': 'WeatherApp/1.0'}
        if user_headers:
            headers.update(user_headers)
            
        try:
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None

    def get_temperature(self, city, user_headers=None):
        """Get temperature for a city in Celsius"""
        weather_data = self.get_weather(city, user_headers)
        if weather_data and 'current' in weather_data:
            return weather_data['current']['temp_c']
        return None
