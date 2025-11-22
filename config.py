import os

class Config:
    SECRET_KEY = os.getenv('123', 'your-secret-key-here')
    USDA_API_KEY = os.getenv('t1brQhOlyvWGeAUfG8nJIrbi966eNpfJQEeXKDho')
    DEBUG = False
    TESTING = False
