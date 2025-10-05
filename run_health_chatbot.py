#!/usr/bin/env python3
"""
Quick launcher for the Simple Health Assistant
This script provides an easy way to run the simplified health-focused chatbot
"""

import subprocess
import sys
import os

def main():
    """
    Launch the Simple Health Assistant
    """
    print("Starting Simple Health Assistant...")
    print("=" * 50)
    print("This chatbot is specifically designed for people 30+")
    print("Features:")
    print("• Personalized health advice")
    print("• Direct and concise responses")
    print("• Focus on core health topics")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Check if health chatbot script exists
    if not os.path.exists("streamlit_health_chatbot.py"):
        print("❌ streamlit_health_chatbot.py not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Launch the health chatbot
    try:
        print("\n🚀 Launching Simple Health Assistant...")
        print("The app will open in your web browser at http://localhost:8501")
        print("\nPress Ctrl+C to stop the application")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_health_chatbot.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Simple Health Assistant stopped.")
        print("Thank you for using the health chatbot!")
    except Exception as e:
        print(f"❌ Error launching the application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a Google AI API key")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Ensure you're in the correct directory")

if __name__ == "__main__":
    main()
