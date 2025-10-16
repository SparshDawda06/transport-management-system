#!/usr/bin/env python3
"""
Simple script to populate the database with sample data.
Run this script to add example data for all fields in the Transport Management System.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.sample_data import create_sample_data

def main():
    """Main function to run the sample data generation."""
    print("🚀 Transport Management System - Sample Data Generator")
    print("=" * 60)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Run the sample data creation
            create_sample_data()
            print("\n✅ Sample data generation completed successfully!")
            print("\n📋 You can now:")
            print("   • Start the application: python3 run.py")
            print("   • Access the web interface at: http://localhost:8000")
            print("   • Login with: admin / admin123")
            print("\n🎉 Enjoy exploring the Transport Management System!")
            
        except Exception as e:
            print(f"\n❌ Error occurred while creating sample data: {e}")
            print("Please check your database configuration and try again.")
            sys.exit(1)

if __name__ == "__main__":
    main()
