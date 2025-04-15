# test_app.py - Unit tests for the WeatherService
import unittest
from unittest.mock import patch, MagicMock
from app import WeatherService

class TestWeatherService(unittest.TestCase):
    
    def setUp(self):
        self.weather_service = WeatherService(api_key="fake_api_key")
    
    @patch('app.requests.get')
    def test_get_weather_success(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "location": {"name": "London", "country": "UK"},
            "current": {"temp_c": 15.0, "condition": {"text": "Partly cloudy"}}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test
        result = self.weather_service.get_weather("London")
        
        # Verify
        self.assertEqual(result["location"]["name"], "London")
        self.assertEqual(result["current"]["temp_c"], 15.0)
        mock_get.assert_called_once()
    
    @patch('app.requests.get')
    def test_get_weather_with_user_headers(self, mock_get):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"current": {"temp_c": 15.0}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test
        user_headers = {"X-Custom-Header": "value"}
        self.weather_service.get_weather("London", user_headers)
        
        # Verify headers were passed correctly
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["headers"]["X-Custom-Header"], "value")
        self.assertEqual(kwargs["headers"]["User-Agent"], "WeatherApp/1.0")
    
    @patch('app.requests.get')
    def test_get_temperature(self, mock_get):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"current": {"temp_c": 25.5}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test
        result = self.weather_service.get_temperature("Sydney")
        
        # Verify
        self.assertEqual(result, 25.5)
    
    @patch('app.requests.get')
    def test_get_weather_error(self, mock_get):
        # Setup mock to raise exception
        mock_get.side_effect = Exception("Connection error")
        
        # Test
        result = self.weather_service.get_weather("London")
        
        # Verify
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
