"""
Movie Booking Plugin for Cog AI Agent
Handles movie ticket booking from platforms like BookMyShow
"""

import asyncio
import json
import uuid
from typing import Dict, List, Any
from datetime import datetime, timedelta
from plugins.plugin_manager import BasePlugin

class MovieBookingPlugin(BasePlugin):
    """Plugin for booking movie tickets"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "MovieBookingPlugin"
        self.version = "1.0.0"
        self.description = "Books movie tickets from various platforms"
        self.supported_intents = ["movie_booking"]
        
        # Platform configurations
        self.platforms = {
            'bookmyshow': {
                'url': 'https://in.bookmyshow.com',
                'name': 'BookMyShow'
            },
            'paytm': {
                'url': 'https://paytm.com/movies',
                'name': 'Paytm Movies'
            },
            'fandango': {
                'url': 'https://www.fandango.com',
                'name': 'Fandango'
            }
        }
        
        # Mock movie data
        self.current_movies = [
            {
                "title": "Avengers: Endgame",
                "genre": "Action/Adventure",
                "duration": "181 minutes",
                "rating": "PG-13",
                "language": "English",
                "theaters": ["PVR Cinemas", "INOX", "Cinepolis"]
            },
            {
                "title": "Spider-Man: No Way Home",
                "genre": "Action/Adventure",
                "duration": "148 minutes",
                "rating": "PG-13",
                "language": "English",
                "theaters": ["PVR Cinemas", "INOX"]
            },
            {
                "title": "The Batman",
                "genre": "Action/Crime",
                "duration": "176 minutes",
                "rating": "PG-13",
                "language": "English",
                "theaters": ["PVR Cinemas", "Cinepolis"]
            }
        ]
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.supported_intents
    
    async def initialize(self) -> bool:
        """Initialize the movie booking plugin"""
        try:
            self.logger.info("Movie booking plugin initialized")
            return True
        except Exception as e:
            self.logger.error(f"Error initializing movie booking plugin: {e}")
            return False
    
    async def execute(self, intent: str, parameters: Dict[str, Any], command: str) -> Dict[str, Any]:
        """Execute movie booking"""
        try:
            movie_name = parameters.get('movie_name', 'latest movie')
            time = parameters.get('time', 'evening')
            location = parameters.get('location', 'current location')
            platform = parameters.get('platform', 'bookmyshow').lower()
            
            if platform not in self.platforms:
                return {
                    "success": False,
                    "error": f"Platform {platform} not supported",
                    "supported_platforms": list(self.platforms.keys())
                }
            
            # Find movie
            movie = await self._find_movie(movie_name)
            if not movie:
                return {
                    "success": False,
                    "error": f"Movie '{movie_name}' not found",
                    "available_movies": [m['title'] for m in self.current_movies]
                }
            
            # Simulate booking process
            result = await self._simulate_movie_booking(movie, time, location, platform)
            
            return {
                "success": True,
                "message": f"Movie ticket booked successfully on {self.platforms[platform]['name']}",
                "booking_details": result,
                "task_created": True
            }
            
        except Exception as e:
            self.logger.error(f"Error executing movie booking: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _find_movie(self, movie_name: str) -> Dict[str, Any]:
        """Find movie by name"""
        movie_name_lower = movie_name.lower()
        
        for movie in self.current_movies:
            if movie_name_lower in movie['title'].lower():
                return movie
        
        return None
    
    async def _simulate_movie_booking(self, movie: Dict[str, Any], time: str, location: str, platform: str) -> Dict[str, Any]:
        """Simulate movie booking process"""
        
        # Simulate processing time
        await asyncio.sleep(2)
        
        # Generate mock booking details
        booking_id = f"BMS_{uuid.uuid4().hex[:8].upper()}"
        
        # Generate show times
        show_times = self._generate_show_times(time)
        selected_time = show_times[0] if show_times else "7:00 PM"
        
        # Select theater
        theater = movie['theaters'][0] if movie['theaters'] else "PVR Cinemas"
        
        # Generate seat selection
        seats = ["F12", "F13"]
        
        # Calculate pricing
        base_price = 200
        convenience_fee = 30
        taxes = 20
        total_per_ticket = base_price + convenience_fee + taxes
        total_amount = total_per_ticket * len(seats)
        
        return {
            "booking_id": booking_id,
            "platform": self.platforms[platform]['name'],
            "movie": {
                "title": movie['title'],
                "genre": movie['genre'],
                "duration": movie['duration'],
                "rating": movie['rating'],
                "language": movie['language']
            },
            "theater": theater,
            "location": location,
            "show_time": selected_time,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "seats": seats,
            "pricing": {
                "base_price": base_price,
                "convenience_fee": convenience_fee,
                "taxes": taxes,
                "total_per_ticket": total_per_ticket,
                "number_of_tickets": len(seats),
                "total_amount": total_amount,
                "currency": "₹"
            },
            "status": "Booking Confirmed",
            "payment_method": "Credit Card",
            "booking_time": datetime.now().isoformat()
        }
    
    def _generate_show_times(self, preferred_time: str) -> List[str]:
        """Generate show times based on preferred time"""
        if "morning" in preferred_time.lower():
            return ["10:00 AM", "11:30 AM"]
        elif "afternoon" in preferred_time.lower():
            return ["1:00 PM", "2:30 PM", "4:00 PM"]
        elif "evening" in preferred_time.lower():
            return ["7:00 PM", "8:30 PM", "10:00 PM"]
        elif "night" in preferred_time.lower():
            return ["9:30 PM", "10:30 PM"]
        else:
            # Default times
            return ["7:00 PM", "10:00 PM"]
    
    async def get_current_movies(self, location: str = None) -> List[Dict[str, Any]]:
        """Get list of current movies"""
        return self.current_movies
    
    async def get_theaters(self, location: str) -> List[Dict[str, Any]]:
        """Get list of theaters in location"""
        theaters = [
            {
                "name": "PVR Cinemas",
                "location": location,
                "screens": 8,
                "facilities": ["Parking", "Food Court", "3D", "IMAX"]
            },
            {
                "name": "INOX",
                "location": location,
                "screens": 6,
                "facilities": ["Parking", "Food Court", "3D"]
            },
            {
                "name": "Cinepolis",
                "location": location,
                "screens": 10,
                "facilities": ["Parking", "Food Court", "3D", "4DX"]
            }
        ]
        return theaters
    
    async def get_show_times(self, movie_title: str, theater: str, date: str = None) -> List[str]:
        """Get show times for a movie at a theater"""
        return ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"]
    
    async def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """Cancel a movie booking"""
        return {
            "success": True,
            "booking_id": booking_id,
            "status": "Cancelled",
            "refund_amount": "₹500",
            "refund_status": "Refund will be processed in 3-5 business days"
        }
    
    async def get_booking_details(self, booking_id: str) -> Dict[str, Any]:
        """Get booking details"""
        return {
            "booking_id": booking_id,
            "movie": "Sample Movie",
            "theater": "PVR Cinemas",
            "show_time": "7:00 PM",
            "seats": ["F12", "F13"],
            "total_amount": "₹500",
            "status": "Confirmed"
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Movie booking plugin cleaned up")