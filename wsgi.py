"""
WSGI Entry Point for Farm Financial Intelligence Platform
Used by Gunicorn for production deployment
"""

from app import app

if __name__ == "__main__":
    app.run()
