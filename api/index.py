import sys
import os
from pathlib import Path

# Add the parent directory to the path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Flask app
try:
    from app import app
except Exception as e:
    # If import fails, create a minimal error reporting app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'error': f'Failed to import main app: {str(e)}',
            'sys_path': sys.path,
            'cwd': os.getcwd(),
            'parent_dir': parent_dir,
            'files_in_parent': os.listdir(parent_dir) if os.path.exists(parent_dir) else 'N/A'
        }), 500

# Vercel expects a WSGI app variable named 'app'
