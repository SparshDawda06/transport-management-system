#!/usr/bin/env python3
"""
Demo script to show the sample data in the Transport Management System.
This script demonstrates how to access and display the sample data.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import (
    Station, PinCode, Consignor, Consignee, BookingAgent, Goods, 
    Owner, Driver, Vehicle, Order, Builty, ConcernedPerson, PhoneBook
)

def demo_sample_data():
    """Demonstrate the sample data in the database."""
    print("🚀 Transport Management System - Sample Data Demo")
    print("=" * 60)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Display counts
            print("\n📊 Database Statistics:")
            print(f"   • Stations: {Station.query.count()}")
            print(f"   • Pin Codes: {PinCode.query.count()}")
            print(f"   • Goods: {Goods.query.count()}")
            print(f"   • Consignors: {Consignor.query.count()}")
            print(f"   • Consignees: {Consignee.query.count()}")
            print(f"   • Booking Agents: {BookingAgent.query.count()}")
            print(f"   • Owners: {Owner.query.count()}")
            print(f"   • Drivers: {Driver.query.count()}")
            print(f"   • Vehicles: {Vehicle.query.count()}")
            print(f"   • Orders: {Order.query.count()}")
            print(f"   • Builty Records: {Builty.query.count()}")
            print(f"   • Concerned Persons: {ConcernedPerson.query.count()}")
            print(f"   • Phone Book Entries: {PhoneBook.query.count()}")
            
            # Display sample stations
            print("\n🏢 Sample Stations:")
            for station in Station.query.limit(5):
                print(f"   • {station.name}, {station.state}")
            
            # Display sample consignors
            print("\n📤 Sample Consignors:")
            for consignor in Consignor.query.limit(3):
                print(f"   • {consignor.name} ({consignor.gstin})")
                print(f"     Phone: {consignor.phone}")
                print(f"     Email: {consignor.email}")
            
            # Display sample orders
            print("\n📋 Sample Orders:")
            for order in Order.query.limit(3):
                print(f"   • Order #{order.id} - {order.consignor.name} → {order.consignee.name}")
                print(f"     Date: {order.date}, Status: {order.status}")
                print(f"     Weight: {order.weight} tons, Rate: ₹{order.rate}")
            
            # Display sample vehicles
            print("\n🚛 Sample Vehicles:")
            for vehicle in Vehicle.query.limit(3):
                print(f"   • {vehicle.lorry_no} (Capacity: {vehicle.capacity} tons)")
                print(f"     Owner: {vehicle.owner.name}")
                print(f"     Driver: {vehicle.driver.name}")
            
            print("\n✅ Sample data demonstration completed!")
            print("\n🌐 To explore the full system:")
            print("   1. Start the application: python3 run.py")
            print("   2. Open your browser: http://localhost:8000")
            print("   3. Login with: admin / admin123")
            
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            print("Please run the sample data script first:")
            print("   python3 seed_sample_data.py")
            sys.exit(1)

if __name__ == "__main__":
    demo_sample_data()
