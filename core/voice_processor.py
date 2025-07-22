"""
Voice Processing Module for Cog AI Agent
Handles speech recognition and text-to-speech functionality
"""

import asyncio
import threading
import logging
import queue
from typing import Optional, Callable
import speech_recognition as sr
import pyttsx3
import wave
import pyaudio

class VoiceProcessor:
    """
    Handles all voice-related functionality including:
    - Speech recognition
    - Text-to-speech
    - Wake word detection
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        # Voice settings
        self.listening_timeout = 5.0
        self.phrase_timeout = 1.0
        self.energy_threshold = 300
        
        # Setup microphone
        self._setup_microphone()
        
        self.logger.info("Voice processor initialized")
    
    def _configure_tts(self):
        """Configure text-to-speech engine"""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 180)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
    
    def _setup_microphone(self):
        """Setup microphone for optimal performance"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = self.energy_threshold
                self.logger.info("Microphone setup complete")
        except Exception as e:
            self.logger.error(f"Error setting up microphone: {e}")
    
    def listen_for_command(self, wake_word: str = None) -> Optional[str]:
        """
        Listen for a voice command
        
        Args:
            wake_word: Optional wake word to listen for first
            
        Returns:
            Recognized command text or None
        """
        try:
            with self.microphone as source:
                self.logger.debug("Listening for audio...")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.listening_timeout,
                    phrase_time_limit=self.phrase_timeout
                )
                
                # Recognize speech
                try:
                    command = self.recognizer.recognize_google(audio)
                    self.logger.info(f"Recognized: {command}")
                    
                    # Check for wake word if specified
                    if wake_word and wake_word.lower() not in command.lower():
                        return None
                    
                    # Remove wake word from command
                    if wake_word:
                        command = command.lower().replace(wake_word.lower(), "").strip()
                    
                    return command
                    
                except sr.UnknownValueError:
                    self.logger.debug("Could not understand audio")
                    return None
                except sr.RequestError as e:
                    self.logger.error(f"Error with speech recognition service: {e}")
                    return None
                    
        except sr.WaitTimeoutError:
            self.logger.debug("Listening timeout")
            return None
        except Exception as e:
            self.logger.error(f"Error in voice recognition: {e}")
            return None
    
    async def speak(self, text: str):
        """
        Convert text to speech asynchronously
        
        Args:
            text: Text to speak
        """
        def _speak():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                self.logger.debug(f"Spoke: {text}")
            except Exception as e:
                self.logger.error(f"Error in text-to-speech: {e}")
        
        # Run TTS in a separate thread to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _speak)
    
    def continuous_listen(self, callback: Callable[[str], None], wake_word: str = None):
        """
        Start continuous listening in the background
        
        Args:
            callback: Function to call when command is recognized
            wake_word: Optional wake word to listen for
        """
        def _listen_loop():
            while True:
                try:
                    command = self.listen_for_command(wake_word)
                    if command:
                        callback(command)
                except Exception as e:
                    self.logger.error(f"Error in continuous listening: {e}")
        
        # Start listening in background thread
        listen_thread = threading.Thread(target=_listen_loop, daemon=True)
        listen_thread.start()
        self.logger.info("Started continuous listening")
    
    def record_audio(self, filename: str, duration: int = 5):
        """
        Record audio to a file
        
        Args:
            filename: Output filename
            duration: Recording duration in seconds
        """
        try:
            # Audio recording parameters
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            
            p = pyaudio.PyAudio()
            
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            self.logger.info(f"Recording audio for {duration} seconds...")
            frames = []
            
            for _ in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save audio file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            self.logger.info(f"Audio saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error recording audio: {e}")
    
    def set_voice_settings(self, rate: int = None, volume: float = None):
        """
        Update voice settings
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
            self.logger.info(f"Voice settings updated - Rate: {rate}, Volume: {volume}")
        except Exception as e:
            self.logger.error(f"Error updating voice settings: {e}")
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []
            for voice in voices:
                voice_list.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
                })
            return voice_list
        except Exception as e:
            self.logger.error(f"Error getting available voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """
        Set TTS voice by ID
        
        Args:
            voice_id: Voice identifier
        """
        try:
            self.tts_engine.setProperty('voice', voice_id)
            self.logger.info(f"Voice set to: {voice_id}")
        except Exception as e:
            self.logger.error(f"Error setting voice: {e}")