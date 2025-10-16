# Sample Data for Transport Management System

This document describes the sample data that can be populated in the Transport Management System database.

## 🚀 Quick Start

### Option 1: Using the Simple Script
```bash
python3 seed_sample_data.py
```

### Option 2: Using Flask CLI
```bash
FLASK_APP=run.py flask seed-data
```

### Option 3: Using Python Directly
```bash
python3 -c "from app import create_app; from app.sample_data import create_sample_data; app = create_app(); app.app_context().push(); create_sample_data()"
```

## 📊 Enhanced Sample Data Overview

The comprehensive sample data includes realistic examples for all major entities with status interactions:

### 🏢 Stations (20 stations)
- Major Indian railway stations across different states
- Mumbai Central, Delhi Junction, Bangalore City, Chennai Central, Kolkata Howrah, etc.
- Includes stations from Gujarat, Maharashtra, Karnataka, Tamil Nadu, West Bengal, Rajasthan, UP, MP, Kerala, Telangana
- Each station includes state information

### 📮 Pin Codes (50+ pin codes)
- Realistic Indian pin codes linked to stations
- Covers major metropolitan areas and tier-2 cities
- Includes state and station associations
- Multiple pin codes per station for comprehensive coverage

### 📦 Goods (20 categories)
- Comprehensive transportation goods categories
- Textiles, Electronics, Food, Pharmaceuticals, Automotive Parts, Construction Materials, Agricultural Products, Chemicals, Furniture, Books, Machinery, Medical Devices, Cosmetics, Sports Equipment, Jewelry, Paper, Rubber, Metal, Glass, Leather
- Realistic descriptions for each category

### 📤 Consignors (10 companies)
- Major Indian companies: Reliance, Tata Motors, Infosys, Wipro, HUL, Mahindra, BPCL, ITC, L&T, Airtel
- Complete business information including GSTIN, PAN, addresses
- Contact details and holiday information
- Geographic distribution across major cities

### 📥 Consignees (10 companies)
- E-commerce and retail companies: Amazon, Flipkart, BigBasket, Reliance Retail, Future Group, DMart, Spencer's, Vijay Sales, Croma, Myntra
- Complete business information with contact details
- Realistic addresses and contact information
- Mix of online and offline retailers

### 🏢 Booking Agents (10 agents)
- Transportation and logistics companies across different cities
- Speed Logistics, Express Cargo, Fast Track, Quick Move, Rapid Transport, Swift Logistics, Reliable Transport, Efficient Cargo, Professional Logistics, Trusted Transport
- Complete business information with GSTIN and PAN
- Contact details and location information

### 👤 Vehicle Owners (10 owners)
- Individual vehicle owners with complete details
- PAN, Aadhar, and contact information
- Realistic addresses across different cities
- Geographic distribution for fleet management

### 🚗 Drivers (10 drivers)
- Professional drivers with valid licenses
- Complete license information with validity dates
- Aadhar and contact details
- Different RTO jurisdictions and license validity periods

### 🚛 Vehicles (10 vehicles)
- Different types of commercial vehicles
- Realistic registration numbers and capacity information
- Chassis and engine numbers
- Linked to owners and drivers
- Various capacity ranges (7-12 tons)

### 👥 Concerned Persons
- Contact persons for all entities (consignors, consignees, agents, drivers, owners)
- Designation and role information
- Primary contact person designation
- Complete relationship mapping

### 📞 Phone Book
- Multiple phone numbers for each concerned person
- Primary and secondary numbers
- Different labels (Mobile, Office, Home)
- Comprehensive contact management

### 📋 Orders (25 orders)
- Orders spanning the last 30 days with realistic scenarios
- Mix of PARTY and AGENT order types
- **Status Distribution:**
  - NEW: 5 orders (recent, urgent shipments)
  - IN_PROGRESS: 5 orders (active transportation)
  - COMPLETED: 15 orders (successful deliveries)
  - CANCELLED: 3 orders (various cancellation reasons)
- Realistic weight, rates, and descriptions
- Linked to all relevant entities

### 📄 Builty Records (18 records)
- Delivery receipts with status interactions
- **Status Distribution:**
  - IN_TRANSIT: 5 records (active transportation)
  - DELIVERED: 10 records (completed deliveries)
  - PENDING: 3 records (awaiting assignment)
- LR numbers, invoice numbers, e-way bill numbers
- Actual and charged weights with realistic variations
- Advance amounts based on status

### 📊 Transaction Logs (100+ logs)
- Comprehensive activity logs for all entities
- **Status Transition Tracking:**
  - Order creation and status updates
  - Builty creation and status changes
  - Entity interactions and updates
- Timestamps and detailed action descriptions
- Complete audit trail showing business workflows

## 🔧 Data Relationships

The sample data maintains proper relationships between all entities:

- **Orders** are linked to consignors, consignees, agents, goods, and stations
- **Builty** records are linked to orders, vehicles, drivers, and owners
- **Phone Book** entries are linked to concerned persons
- **Concerned Persons** are linked to their respective entities
- **Vehicles** are linked to owners and drivers
- **Pin Codes** are linked to stations

## 🎯 Use Cases

This sample data allows you to:

1. **Test Order Management**: Create, view, and manage transportation orders
2. **Test Fleet Management**: Manage vehicles, drivers, and owners
3. **Test Entity Management**: Work with consignors, consignees, and agents
4. **Test Phone Book**: Manage contact information and concerned persons
5. **Test Builty Management**: Create and manage delivery receipts
6. **Test System Configuration**: Work with stations, goods, and pin codes

## 🚨 Important Notes

- The sample data script will **clear existing data** before adding new data
- All data is realistic but fictional
- GSTIN, PAN, and Aadhar numbers are examples only
- Phone numbers and addresses are fictional
- License numbers and vehicle registrations are examples

## 🔄 Regenerating Data

To regenerate the sample data:

1. **Clear existing data**: The script automatically clears existing data
2. **Run the script**: Use any of the methods mentioned above
3. **Verify data**: Check the web interface to ensure data is populated

## 🛠️ Customization

You can modify the sample data by editing `app/sample_data.py`:

- Add more entities by extending the data arrays
- Modify existing data to match your requirements
- Add new entity types following the existing patterns
- Customize the relationships between entities

## 📱 Accessing the Data

After running the sample data script:

1. Start the application: `python3 run.py`
2. Open your browser: `http://localhost:8000`
3. Login with: `admin` / `admin123`
4. Navigate through the different sections to see the sample data

## 🎉 Enjoy!

The sample data provides a comprehensive foundation for exploring and testing the Transport Management System. All major features and workflows can be tested with realistic data.
