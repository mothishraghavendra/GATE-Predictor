import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# This is the entry point for Vercel
# Vercel expects a variable named 'app' or a handler function
handler = app

# For local testing
if __name__ == '__main__':
    app.run()
