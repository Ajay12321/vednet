"""
GUI Interface for Cog AI Agent
Provides a graphical user interface for interacting with the agent
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import asyncio
from typing import Dict, Any
import json

class GUIInterface:
    """GUI Interface for Cog AI Agent"""
    
    def __init__(self, agent):
        self.agent = agent
        self.root = None
        self.command_entry = None
        self.response_area = None
        self.status_label = None
        self.voice_button = None
        
    def run(self):
        """Run the GUI"""
        try:
            self.root = tk.Tk()
            self.root.title("Cog AI Assistant")
            self.root.geometry("800x600")
            self.root.configure(bg="#2c3e50")
            
            self._create_widgets()
            self._setup_layout()
            
            # Start the main loop
            self.root.mainloop()
            
        except Exception as e:
            print(f"Error running GUI: {e}")
    
    def _create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="Cog AI Assistant", 
            font=("Arial", 24, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg="#2c3e50")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=("Arial", 12),
            fg="#27ae60",
            bg="#2c3e50"
        )
        self.status_label.pack(side="left")
        
        # Voice toggle button
        self.voice_button = tk.Button(
            status_frame,
            text="🎤 Voice: ON" if self.agent.is_listening else "🎤 Voice: OFF",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            command=self._toggle_voice,
            relief="flat",
            padx=20
        )
        self.voice_button.pack(side="right")
        
        # Response area
        response_label = tk.Label(
            self.root,
            text="Conversation:",
            font=("Arial", 14, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        response_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.response_area = scrolledtext.ScrolledText(
            self.root,
            height=20,
            width=80,
            font=("Arial", 11),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            wrap=tk.WORD
        )
        self.response_area.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Command input frame
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(fill="x", padx=20, pady=20)
        
        # Command entry
        self.command_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            relief="flat",
            bd=5
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.command_entry.bind("<Return>", self._on_enter_pressed)
        
        # Send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=self._send_command,
            relief="flat",
            padx=20
        )
        send_button.pack(side="right")
        
        # Menu bar
        self._create_menu()
        
        # Add welcome message
        self._add_message("Cog", "Hello! I'm Cog, your AI assistant. How can I help you today?", "#3498db")
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Chat", command=self._clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Voice Settings", command=self._show_voice_settings)
        settings_menu.add_command(label="API Settings", command=self._show_api_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Commands", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _setup_layout(self):
        """Setup the layout"""
        # Focus on command entry
        self.command_entry.focus_set()
    
    def _toggle_voice(self):
        """Toggle voice listening"""
        self.agent.toggle_listening()
        self.voice_button.config(
            text="🎤 Voice: ON" if self.agent.is_listening else "🎤 Voice: OFF",
            bg="#27ae60" if self.agent.is_listening else "#e74c3c"
        )
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press"""
        self._send_command()
    
    def _send_command(self):
        """Send command to agent"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.command_entry.delete(0, tk.END)
        
        # Add user message to chat
        self._add_message("You", command, "#e74c3c")
        
        # Update status
        self.status_label.config(text="Status: Processing...", fg="#f39c12")
        
        # Process command in background thread
        threading.Thread(
            target=self._process_command_async,
            args=(command,),
            daemon=True
        ).start()
    
    def _process_command_async(self, command: str):
        """Process command asynchronously"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Process command
            result = loop.run_until_complete(
                self.agent.process_command(command, source="text")
            )
            
            # Update GUI in main thread
            self.root.after(0, self._handle_command_result, result)
            
        except Exception as e:
            error_msg = f"Error processing command: {e}"
            self.root.after(0, self._handle_command_error, error_msg)
    
    def _handle_command_result(self, result: Dict[str, Any]):
        """Handle command result"""
        response = result.get('response', 'Command processed successfully')
        
        # Add response to chat
        self._add_message("Cog", response, "#3498db")
        
        # Update status
        if result.get('success', True):
            self.status_label.config(text="Status: Ready", fg="#27ae60")
        else:
            self.status_label.config(text="Status: Error", fg="#e74c3c")
        
        # Show additional info if available
        if result.get('task_created'):
            self._add_message("System", "Task created and will be executed", "#9b59b6")
    
    def _handle_command_error(self, error_msg: str):
        """Handle command error"""
        self._add_message("System", error_msg, "#e74c3c")
        self.status_label.config(text="Status: Error", fg="#e74c3c")
    
    def _add_message(self, sender: str, message: str, color: str):
        """Add message to conversation area"""
        self.response_area.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Format message
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        # Insert message with color
        self.response_area.insert(tk.END, formatted_message)
        
        # Apply color to sender name
        start_line = self.response_area.index(tk.END).split('.')[0]
        start_pos = f"{int(start_line)-2}.{len(timestamp)+3}"
        end_pos = f"{int(start_line)-2}.{len(timestamp)+3+len(sender)}"
        
        tag_name = f"sender_{sender}_{timestamp}"
        self.response_area.tag_add(tag_name, start_pos, end_pos)
        self.response_area.tag_config(tag_name, foreground=color, font=("Arial", 11, "bold"))
        
        # Scroll to bottom
        self.response_area.see(tk.END)
        self.response_area.config(state=tk.DISABLED)
    
    def _clear_chat(self):
        """Clear chat history"""
        self.response_area.config(state=tk.NORMAL)
        self.response_area.delete(1.0, tk.END)
        self.response_area.config(state=tk.DISABLED)
        self._add_message("Cog", "Chat cleared. How can I help you?", "#3498db")
    
    def _show_voice_settings(self):
        """Show voice settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Voice Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#2c3e50")
        
        # Voice settings content
        tk.Label(
            settings_window,
            text="Voice Settings",
            font=("Arial", 16, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(pady=20)
        
        # Wake word setting
        tk.Label(
            settings_window,
            text="Wake Word:",
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(anchor="w", padx=20)
        
        wake_word_entry = tk.Entry(settings_window, font=("Arial", 12))
        wake_word_entry.pack(fill="x", padx=20, pady=5)
        wake_word_entry.insert(0, self.agent.wake_word)
        
        # Voice rate setting
        tk.Label(
            settings_window,
            text="Speech Rate:",
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(anchor="w", padx=20, pady=(20, 0))
        
        rate_scale = tk.Scale(
            settings_window,
            from_=100,
            to=300,
            orient=tk.HORIZONTAL,
            bg="#34495e",
            fg="#ecf0f1"
        )
        rate_scale.pack(fill="x", padx=20, pady=5)
        rate_scale.set(180)
        
        # Save button
        def save_voice_settings():
            self.agent.wake_word = wake_word_entry.get()
            # Update voice processor settings
            settings_window.destroy()
            messagebox.showinfo("Settings", "Voice settings saved!")
        
        tk.Button(
            settings_window,
            text="Save",
            command=save_voice_settings,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)
    
    def _show_api_settings(self):
        """Show API settings dialog"""
        messagebox.showinfo("API Settings", "Configure API keys in the .env file or config.json")
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
Available Commands:

🍕 Food Ordering:
- "Order pizza from Swiggy"
- "Get me biryani from Zomato"

🎬 Movie Booking:
- "Book tickets for Avengers"
- "Movie ticket for tonight"

🛒 Shopping:
- "Buy a red dress from Amazon"
- "Order phone from Flipkart"

📅 Reminders:
- "Remind me to call mom at 3 PM"
- "Set reminder for tomorrow"

🌤️ Weather & News:
- "What's the weather?"
- "Get latest news"

💬 General:
- "Help" - Show this help
- "Status" - Show system status
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Cog Commands")
        help_window.geometry("500x600")
        help_window.configure(bg="#2c3e50")
        
        help_text_widget = scrolledtext.ScrolledText(
            help_window,
            font=("Arial", 11),
            bg="#34495e",
            fg="#ecf0f1",
            wrap=tk.WORD
        )
        help_text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """
Cog AI Assistant v1.0

A comprehensive AI assistant that can:
• Order food from delivery apps
• Book movie tickets
• Shop online
• Set reminders
• Get weather and news
• Much more!

Powered by Python, OpenAI, and advanced NLP.
        """
        messagebox.showinfo("About Cog", about_text)