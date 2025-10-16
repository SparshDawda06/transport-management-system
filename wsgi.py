#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
from app import create_app
from app.config import ProductionConfig

# Create Flask app with production configuration
application = create_app(ProductionConfig)

if __name__ == "__main__":
    application.run()
