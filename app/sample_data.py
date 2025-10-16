"""
Sample Data Generator for Transport Management System
This script populates the database with realistic sample data for all entities.
"""

from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    Station, PinCode, Consignor, Consignee, BookingAgent, Goods, 
    Owner, Driver, Vehicle, Order, Builty, ConcernedPerson, PhoneBook,
    TransactionLog
)
import random


def create_sample_data():
    """Create comprehensive sample data for all models"""
    
    print("🚀 Creating sample data for Transport Management System...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("🧹 Clearing existing data...")
    db.drop_all()
    db.create_all()
    
    # 1. Create Stations
    print("🏢 Creating stations...")
    stations_data = [
        {"name": "Mumbai Central", "state": "Maharashtra"},
        {"name": "Delhi Junction", "state": "Delhi"},
        {"name": "Bangalore City", "state": "Karnataka"},
        {"name": "Chennai Central", "state": "Tamil Nadu"},
        {"name": "Kolkata Howrah", "state": "West Bengal"},
        {"name": "Ahmedabad Junction", "state": "Gujarat"},
        {"name": "Pune Junction", "state": "Maharashtra"},
        {"name": "Hyderabad Deccan", "state": "Telangana"},
        {"name": "Jaipur Junction", "state": "Rajasthan"},
        {"name": "Lucknow Charbagh", "state": "Uttar Pradesh"},
        {"name": "Surat Junction", "state": "Gujarat"},
        {"name": "Nagpur Junction", "state": "Maharashtra"},
        {"name": "Indore Junction", "state": "Madhya Pradesh"},
        {"name": "Bhopal Junction", "state": "Madhya Pradesh"},
        {"name": "Vadodara Junction", "state": "Gujarat"},
        {"name": "Coimbatore Junction", "state": "Tamil Nadu"},
        {"name": "Kochi Junction", "state": "Kerala"},
        {"name": "Trivandrum Central", "state": "Kerala"},
        {"name": "Mysore Junction", "state": "Karnataka"},
        {"name": "Hubli Junction", "state": "Karnataka"},
    ]
    
    stations = []
    for station_data in stations_data:
        station = Station(**station_data)
        db.session.add(station)
        stations.append(station)
    
    db.session.commit()
    print(f"✅ Created {len(stations)} stations")
    
    # 2. Create Pin Codes
    print("📮 Creating pin codes...")
    pin_codes_data = [
        # Mumbai
        {"code": "400001", "state": "Maharashtra", "station_id": stations[0].id},
        {"code": "400002", "state": "Maharashtra", "station_id": stations[0].id},
        {"code": "400003", "state": "Maharashtra", "station_id": stations[0].id},
        # Delhi
        {"code": "110001", "state": "Delhi", "station_id": stations[1].id},
        {"code": "110002", "state": "Delhi", "station_id": stations[1].id},
        {"code": "110003", "state": "Delhi", "station_id": stations[1].id},
        # Bangalore
        {"code": "560001", "state": "Karnataka", "station_id": stations[2].id},
        {"code": "560002", "state": "Karnataka", "station_id": stations[2].id},
        {"code": "560003", "state": "Karnataka", "station_id": stations[2].id},
        # Chennai
        {"code": "600001", "state": "Tamil Nadu", "station_id": stations[3].id},
        {"code": "600002", "state": "Tamil Nadu", "station_id": stations[3].id},
        {"code": "600003", "state": "Tamil Nadu", "station_id": stations[3].id},
        # Kolkata
        {"code": "700001", "state": "West Bengal", "station_id": stations[4].id},
        {"code": "700002", "state": "West Bengal", "station_id": stations[4].id},
        {"code": "700003", "state": "West Bengal", "station_id": stations[4].id},
        # Ahmedabad
        {"code": "380001", "state": "Gujarat", "station_id": stations[5].id},
        {"code": "380002", "state": "Gujarat", "station_id": stations[5].id},
        {"code": "380003", "state": "Gujarat", "station_id": stations[5].id},
        # Pune
        {"code": "411001", "state": "Maharashtra", "station_id": stations[6].id},
        {"code": "411002", "state": "Maharashtra", "station_id": stations[6].id},
        {"code": "411003", "state": "Maharashtra", "station_id": stations[6].id},
        # Hyderabad
        {"code": "500001", "state": "Telangana", "station_id": stations[7].id},
        {"code": "500002", "state": "Telangana", "station_id": stations[7].id},
        {"code": "500003", "state": "Telangana", "station_id": stations[7].id},
        # Jaipur
        {"code": "302001", "state": "Rajasthan", "station_id": stations[8].id},
        {"code": "302002", "state": "Rajasthan", "station_id": stations[8].id},
        {"code": "302003", "state": "Rajasthan", "station_id": stations[8].id},
        # Lucknow
        {"code": "226001", "state": "Uttar Pradesh", "station_id": stations[9].id},
        {"code": "226002", "state": "Uttar Pradesh", "station_id": stations[9].id},
        {"code": "226003", "state": "Uttar Pradesh", "station_id": stations[9].id},
        # Surat
        {"code": "395001", "state": "Gujarat", "station_id": stations[10].id},
        {"code": "395002", "state": "Gujarat", "station_id": stations[10].id},
        # Nagpur
        {"code": "440001", "state": "Maharashtra", "station_id": stations[11].id},
        {"code": "440002", "state": "Maharashtra", "station_id": stations[11].id},
        # Indore
        {"code": "452001", "state": "Madhya Pradesh", "station_id": stations[12].id},
        {"code": "452002", "state": "Madhya Pradesh", "station_id": stations[12].id},
        # Bhopal
        {"code": "462001", "state": "Madhya Pradesh", "station_id": stations[13].id},
        {"code": "462002", "state": "Madhya Pradesh", "station_id": stations[13].id},
        # Vadodara
        {"code": "390001", "state": "Gujarat", "station_id": stations[14].id},
        {"code": "390002", "state": "Gujarat", "station_id": stations[14].id},
        # Coimbatore
        {"code": "641001", "state": "Tamil Nadu", "station_id": stations[15].id},
        {"code": "641002", "state": "Tamil Nadu", "station_id": stations[15].id},
        # Kochi
        {"code": "682001", "state": "Kerala", "station_id": stations[16].id},
        {"code": "682002", "state": "Kerala", "station_id": stations[16].id},
        # Trivandrum
        {"code": "695001", "state": "Kerala", "station_id": stations[17].id},
        {"code": "695002", "state": "Kerala", "station_id": stations[17].id},
        # Mysore
        {"code": "570001", "state": "Karnataka", "station_id": stations[18].id},
        {"code": "570002", "state": "Karnataka", "station_id": stations[18].id},
        # Hubli
        {"code": "580001", "state": "Karnataka", "station_id": stations[19].id},
        {"code": "580002", "state": "Karnataka", "station_id": stations[19].id},
    ]
    
    pin_codes = []
    for pin_data in pin_codes_data:
        pin_code = PinCode(**pin_data)
        db.session.add(pin_code)
        pin_codes.append(pin_code)
    
    db.session.commit()
    print(f"✅ Created {len(pin_codes)} pin codes")
    
    # 3. Create Goods
    print("📦 Creating goods...")
    goods_data = [
        {"description": "Textiles and Garments"},
        {"description": "Electronics and Appliances"},
        {"description": "Food and Beverages"},
        {"description": "Pharmaceuticals"},
        {"description": "Automotive Parts"},
        {"description": "Construction Materials"},
        {"description": "Agricultural Products"},
        {"description": "Chemicals"},
        {"description": "Furniture and Home Decor"},
        {"description": "Books and Stationery"},
        {"description": "Machinery and Equipment"},
        {"description": "Medical Devices"},
        {"description": "Cosmetics and Personal Care"},
        {"description": "Sports Equipment"},
        {"description": "Jewelry and Accessories"},
        {"description": "Paper and Packaging"},
        {"description": "Rubber and Plastic Products"},
        {"description": "Metal Products"},
        {"description": "Glass and Ceramics"},
        {"description": "Leather Products"},
    ]
    
    goods = []
    for good_data in goods_data:
        good = Goods(**good_data)
        db.session.add(good)
        goods.append(good)
    
    db.session.commit()
    print(f"✅ Created {len(goods)} goods")
    
    # 4. Create Consignors
    print("📤 Creating consignors...")
    consignors_data = [
        {
            "name": "Reliance Industries Ltd",
            "address": "Reliance Corporate Park, Ghansoli, Navi Mumbai",
            "gstin": "27AABCR1234A1Z5",
            "pan": "AABCR1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[0].id,
            "phone": "+91-22-3555-1000",
            "email": "info@ril.com",
            "holiday_info": "Closed on Sundays and public holidays"
        },
        {
            "name": "Tata Motors Ltd",
            "address": "Bombay House, 24 Homi Mody Street, Mumbai",
            "gstin": "27AABCT1234A1Z5",
            "pan": "AABCT1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[1].id,
            "phone": "+91-22-6665-8282",
            "email": "info@tatamotors.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Infosys Ltd",
            "address": "Electronics City, Hosur Road, Bangalore",
            "gstin": "29AABCI1234A1Z5",
            "pan": "AABCI1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[6].id,
            "phone": "+91-80-2852-0261",
            "email": "info@infosys.com",
            "holiday_info": "Closed on Sundays and public holidays"
        },
        {
            "name": "Wipro Ltd",
            "address": "Doddakannelli, Sarjapur Road, Bangalore",
            "gstin": "29AABCW1234A1Z5",
            "pan": "AABCW1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[7].id,
            "phone": "+91-80-2844-0011",
            "email": "info@wipro.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Hindustan Unilever Ltd",
            "address": "Unilever House, B.D. Sawant Marg, Mumbai",
            "gstin": "27AABCH1234A1Z5",
            "pan": "AABCH1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[2].id,
            "phone": "+91-22-3983-2000",
            "email": "info@hul.co.in",
            "holiday_info": "Closed on Sundays and public holidays"
        },
        {
            "name": "Mahindra & Mahindra Ltd",
            "address": "Gateway Building, Apollo Bunder, Mumbai",
            "gstin": "27AABCM1234A1Z5",
            "pan": "AABCM1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[0].id,
            "phone": "+91-22-2288-5000",
            "email": "info@mahindra.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Bharat Petroleum Corp Ltd",
            "address": "Bharat Bhavan, 4 & 6 Currimbhoy Road, Mumbai",
            "gstin": "27AABCB1234A1Z5",
            "pan": "AABCB1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[1].id,
            "phone": "+91-22-2271-1000",
            "email": "info@bharatpetroleum.com",
            "holiday_info": "Closed on Sundays and public holidays"
        },
        {
            "name": "ITC Ltd",
            "address": "Virginia House, 37 J.L. Nehru Road, Kolkata",
            "gstin": "19AABCI1234A1Z5",
            "pan": "AABCI1234B",
            "station_id": stations[4].id,
            "pin_code_id": pin_codes[13].id,
            "phone": "+91-33-2288-1000",
            "email": "info@itc.in",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Larsen & Toubro Ltd",
            "address": "L&T House, N.M. Marg, Ballard Estate, Mumbai",
            "gstin": "27AABCL1234A1Z5",
            "pan": "AABCL1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[2].id,
            "phone": "+91-22-6752-5656",
            "email": "info@larsentoubro.com",
            "holiday_info": "Closed on Sundays and public holidays"
        },
        {
            "name": "Bharti Airtel Ltd",
            "address": "Airtel Centre, 1 Gurgaon, Haryana",
            "gstin": "06AABCB1234A1Z5",
            "pan": "AABCB1234C",
            "station_id": stations[1].id,
            "pin_code_id": pin_codes[3].id,
            "phone": "+91-11-4300-0000",
            "email": "info@airtel.com",
            "holiday_info": "Open 24/7"
        }
    ]
    
    consignors = []
    for consignor_data in consignors_data:
        consignor = Consignor(**consignor_data)
        db.session.add(consignor)
        consignors.append(consignor)
    
    db.session.commit()
    print(f"✅ Created {len(consignors)} consignors")
    
    # 5. Create Consignees
    print("📥 Creating consignees...")
    consignees_data = [
        {
            "name": "Amazon India Ltd",
            "address": "Amazon Development Centre, Bangalore",
            "gstin": "29AABCA1234A1Z5",
            "pan": "AABCA1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[6].id,
            "phone": "+91-80-4179-1000",
            "email": "info@amazon.in",
            "holiday_info": "Open 24/7"
        },
        {
            "name": "Flipkart Internet Pvt Ltd",
            "address": "Flipkart Internet Pvt Ltd, Bangalore",
            "gstin": "29AABCF1234A1Z5",
            "pan": "AABCF1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[7].id,
            "phone": "+91-80-4179-2000",
            "email": "info@flipkart.com",
            "holiday_info": "Open 24/7"
        },
        {
            "name": "BigBasket",
            "address": "BigBasket, Bangalore",
            "gstin": "29AABCB1234A1Z5",
            "pan": "AABCB1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[8].id,
            "phone": "+91-80-4179-3000",
            "email": "info@bigbasket.com",
            "holiday_info": "Open 24/7"
        },
        {
            "name": "Reliance Retail Ltd",
            "address": "Reliance Retail, Mumbai",
            "gstin": "27AABCRR1234A1Z5",
            "pan": "AABCRR1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[0].id,
            "phone": "+91-22-3555-2000",
            "email": "info@relianceretail.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Future Group",
            "address": "Future Group, Mumbai",
            "gstin": "27AABCFG1234A1Z5",
            "pan": "AABCFG1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[1].id,
            "phone": "+91-22-3555-3000",
            "email": "info@futuregroup.in",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "DMart (Avenue Supermarts Ltd)",
            "address": "Avenue Supermarts Ltd, Mumbai",
            "gstin": "27AABCAV1234A1Z5",
            "pan": "AABCAV1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[2].id,
            "phone": "+91-22-3555-4000",
            "email": "info@dmart.in",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Spencer's Retail Ltd",
            "address": "Spencer's Retail, Kolkata",
            "gstin": "19AABCSR1234A1Z5",
            "pan": "AABCSR1234A",
            "station_id": stations[4].id,
            "pin_code_id": pin_codes[13].id,
            "phone": "+91-33-2288-2000",
            "email": "info@spencersretail.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Vijay Sales",
            "address": "Vijay Sales, Mumbai",
            "gstin": "27AABCVS1234A1Z5",
            "pan": "AABCVS1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[0].id,
            "phone": "+91-22-3555-5000",
            "email": "info@vijaysales.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Croma (Tata Digital)",
            "address": "Croma, Mumbai",
            "gstin": "27AABCCR1234A1Z5",
            "pan": "AABCCR1234A",
            "station_id": stations[0].id,
            "pin_code_id": pin_codes[1].id,
            "phone": "+91-22-3555-6000",
            "email": "info@croma.com",
            "holiday_info": "Closed on Sundays"
        },
        {
            "name": "Myntra (Flipkart)",
            "address": "Myntra, Bangalore",
            "gstin": "29AABCMY1234A1Z5",
            "pan": "AABCMY1234A",
            "station_id": stations[2].id,
            "pin_code_id": pin_codes[6].id,
            "phone": "+91-80-4179-4000",
            "email": "info@myntra.com",
            "holiday_info": "Open 24/7"
        }
    ]
    
    consignees = []
    for consignee_data in consignees_data:
        consignee = Consignee(**consignee_data)
        db.session.add(consignee)
        consignees.append(consignee)
    
    db.session.commit()
    print(f"✅ Created {len(consignees)} consignees")
    
    # 6. Create Booking Agents
    print("🏢 Creating booking agents...")
    agents_data = [
        {
            "name": "Speed Logistics Pvt Ltd",
            "phone": "+91-22-1234-5678",
            "gstin": "27AABCSL1234A1Z5",
            "pan": "AABCSL1234A",
            "station_id": stations[0].id,
            "city": "Mumbai",
            "state": "Maharashtra",
            "email": "info@speedlogistics.com"
        },
        {
            "name": "Express Cargo Services",
            "phone": "+91-11-2345-6789",
            "gstin": "07AABCES1234A1Z5",
            "pan": "AABCES1234A",
            "station_id": stations[1].id,
            "city": "Delhi",
            "state": "Delhi",
            "email": "info@expresscargo.com"
        },
        {
            "name": "Fast Track Transport",
            "phone": "+91-80-3456-7890",
            "gstin": "29AABCFT1234A1Z5",
            "pan": "AABCFT1234A",
            "station_id": stations[2].id,
            "city": "Bangalore",
            "state": "Karnataka",
            "email": "info@fasttrack.com"
        },
        {
            "name": "Quick Move Logistics",
            "phone": "+91-44-4567-8901",
            "gstin": "33AABCQM1234A1Z5",
            "pan": "AABCQM1234A",
            "station_id": stations[3].id,
            "city": "Chennai",
            "state": "Tamil Nadu",
            "email": "info@quickmove.com"
        },
        {
            "name": "Rapid Transport Co",
            "phone": "+91-33-5678-9012",
            "gstin": "19AABCRT1234A1Z5",
            "pan": "AABCRT1234A",
            "station_id": stations[4].id,
            "city": "Kolkata",
            "state": "West Bengal",
            "email": "info@rapidtransport.com"
        },
        {
            "name": "Swift Logistics Solutions",
            "phone": "+91-79-6789-0123",
            "gstin": "24AABCSW1234A1Z5",
            "pan": "AABCSW1234A",
            "station_id": stations[5].id,
            "city": "Ahmedabad",
            "state": "Gujarat",
            "email": "info@swiftlogistics.com"
        },
        {
            "name": "Reliable Transport Services",
            "phone": "+91-20-7890-1234",
            "gstin": "27AABCRL1234A1Z5",
            "pan": "AABCRL1234A",
            "station_id": stations[6].id,
            "city": "Pune",
            "state": "Maharashtra",
            "email": "info@reliabletransport.com"
        },
        {
            "name": "Efficient Cargo Movers",
            "phone": "+91-40-8901-2345",
            "gstin": "36AABCEC1234A1Z5",
            "pan": "AABCEC1234A",
            "station_id": stations[7].id,
            "city": "Hyderabad",
            "state": "Telangana",
            "email": "info@efficientcargo.com"
        },
        {
            "name": "Professional Logistics",
            "phone": "+91-141-9012-3456",
            "gstin": "08AABCPL1234A1Z5",
            "pan": "AABCPL1234A",
            "station_id": stations[8].id,
            "city": "Jaipur",
            "state": "Rajasthan",
            "email": "info@professionallogistics.com"
        },
        {
            "name": "Trusted Transport Co",
            "phone": "+91-522-0123-4567",
            "gstin": "09AABCTT1234A1Z5",
            "pan": "AABCTT1234A",
            "station_id": stations[9].id,
            "city": "Lucknow",
            "state": "Uttar Pradesh",
            "email": "info@trustedtransport.com"
        }
    ]
    
    agents = []
    for agent_data in agents_data:
        agent = BookingAgent(**agent_data)
        db.session.add(agent)
        agents.append(agent)
    
    db.session.commit()
    print(f"✅ Created {len(agents)} booking agents")
    
    # 7. Create Owners
    print("👤 Creating vehicle owners...")
    owners_data = [
        {
            "name": "Rajesh Kumar",
            "phone": "+91-98765-43210",
            "pan": "ABCDR1234A",
            "aadhar": "1234-5678-9012",
            "address": "123, MG Road, Mumbai, Maharashtra - 400001"
        },
        {
            "name": "Suresh Patel",
            "phone": "+91-98765-43211",
            "pan": "ABCDS1234A",
            "aadhar": "1234-5678-9013",
            "address": "456, Park Street, Kolkata, West Bengal - 700001"
        },
        {
            "name": "Amit Singh",
            "phone": "+91-98765-43212",
            "pan": "ABCDA1234A",
            "aadhar": "1234-5678-9014",
            "address": "789, Brigade Road, Bangalore, Karnataka - 560001"
        },
        {
            "name": "Vikram Sharma",
            "phone": "+91-98765-43213",
            "pan": "ABCDV1234A",
            "aadhar": "1234-5678-9015",
            "address": "321, Anna Salai, Chennai, Tamil Nadu - 600001"
        },
        {
            "name": "Ravi Gupta",
            "phone": "+91-98765-43214",
            "pan": "ABCDR1234B",
            "aadhar": "1234-5678-9016",
            "address": "654, CP, Delhi - 110001"
        },
        {
            "name": "Deepak Jain",
            "phone": "+91-98765-43215",
            "pan": "ABCDD1234A",
            "aadhar": "1234-5678-9017",
            "address": "987, C.G. Road, Ahmedabad, Gujarat - 380001"
        },
        {
            "name": "Kiran Reddy",
            "phone": "+91-98765-43216",
            "pan": "ABCDK1234A",
            "aadhar": "1234-5678-9018",
            "address": "654, Banjara Hills, Hyderabad, Telangana - 500001"
        },
        {
            "name": "Prakash Mehta",
            "phone": "+91-98765-43217",
            "pan": "ABCDP1234A",
            "aadhar": "1234-5678-9019",
            "address": "321, Koregaon Park, Pune, Maharashtra - 411001"
        },
        {
            "name": "Sunil Agarwal",
            "phone": "+91-98765-43218",
            "pan": "ABCDS1234B",
            "aadhar": "1234-5678-9020",
            "address": "789, C-Scheme, Jaipur, Rajasthan - 302001"
        },
        {
            "name": "Manoj Tiwari",
            "phone": "+91-98765-43219",
            "pan": "ABCDM1234A",
            "aadhar": "1234-5678-9021",
            "address": "456, Hazratganj, Lucknow, Uttar Pradesh - 226001"
        }
    ]
    
    owners = []
    for owner_data in owners_data:
        owner = Owner(**owner_data)
        db.session.add(owner)
        owners.append(owner)
    
    db.session.commit()
    print(f"✅ Created {len(owners)} owners")
    
    # 8. Create Drivers
    print("🚗 Creating drivers...")
    drivers_data = [
        {
            "name": "Mohammed Ali",
            "address": "123, Dharavi, Mumbai, Maharashtra - 400017",
            "license_no": "MH-01-2015-1234567",
            "validity": date(2025, 12, 31),
            "rto": "Mumbai RTO",
            "aadhar": "1234-5678-9021",
            "phone": "+91-98765-43220"
        },
        {
            "name": "Ram Prasad",
            "address": "456, Salt Lake, Kolkata, West Bengal - 700064",
            "license_no": "WB-01-2016-2345678",
            "validity": date(2026, 6, 30),
            "rto": "Kolkata RTO",
            "aadhar": "1234-5678-9022",
            "phone": "+91-98765-43221"
        },
        {
            "name": "Kumar Swamy",
            "address": "789, Koramangala, Bangalore, Karnataka - 560034",
            "license_no": "KA-01-2017-3456789",
            "validity": date(2027, 3, 15),
            "rto": "Bangalore RTO",
            "aadhar": "1234-5678-9023",
            "phone": "+91-98765-43222"
        },
        {
            "name": "Suresh Kumar",
            "address": "321, T. Nagar, Chennai, Tamil Nadu - 600017",
            "license_no": "TN-01-2018-4567890",
            "validity": date(2028, 9, 20),
            "rto": "Chennai RTO",
            "aadhar": "1234-5678-9024",
            "phone": "+91-98765-43223"
        },
        {
            "name": "Amit Kumar",
            "address": "654, CP, Delhi - 110001",
            "license_no": "DL-01-2019-5678901",
            "validity": date(2029, 1, 10),
            "rto": "Delhi RTO",
            "aadhar": "1234-5678-9025",
            "phone": "+91-98765-43224"
        },
        {
            "name": "Rajesh Patel",
            "address": "987, Maninagar, Ahmedabad, Gujarat - 380008",
            "license_no": "GJ-01-2020-6789012",
            "validity": date(2030, 4, 15),
            "rto": "Ahmedabad RTO",
            "aadhar": "1234-5678-9026",
            "phone": "+91-98765-43225"
        },
        {
            "name": "Venkatesh Reddy",
            "address": "654, Jubilee Hills, Hyderabad, Telangana - 500033",
            "license_no": "TS-01-2021-7890123",
            "validity": date(2031, 7, 25),
            "rto": "Hyderabad RTO",
            "aadhar": "1234-5678-9027",
            "phone": "+91-98765-43226"
        },
        {
            "name": "Prakash Joshi",
            "address": "321, Koregaon Park, Pune, Maharashtra - 411001",
            "license_no": "MH-12-2022-8901234",
            "validity": date(2032, 11, 10),
            "rto": "Pune RTO",
            "aadhar": "1234-5678-9028",
            "phone": "+91-98765-43227"
        },
        {
            "name": "Suresh Agarwal",
            "address": "789, C-Scheme, Jaipur, Rajasthan - 302001",
            "license_no": "RJ-01-2023-9012345",
            "validity": date(2033, 2, 28),
            "rto": "Jaipur RTO",
            "aadhar": "1234-5678-9029",
            "phone": "+91-98765-43228"
        },
        {
            "name": "Manoj Tiwari",
            "address": "456, Hazratganj, Lucknow, Uttar Pradesh - 226001",
            "license_no": "UP-32-2024-0123456",
            "validity": date(2034, 5, 20),
            "rto": "Lucknow RTO",
            "aadhar": "1234-5678-9030",
            "phone": "+91-98765-43229"
        }
    ]
    
    drivers = []
    for driver_data in drivers_data:
        driver = Driver(**driver_data)
        db.session.add(driver)
        drivers.append(driver)
    
    db.session.commit()
    print(f"✅ Created {len(drivers)} drivers")
    
    # 9. Create Vehicles
    print("🚛 Creating vehicles...")
    vehicles_data = [
        {
            "lorry_no": "MH-01-AB-1234",
            "capacity": 9.0,
            "chassis_no": "CH12345678901234567",
            "engine_no": "EN12345678901234567",
            "owner_id": owners[0].id,
            "driver_id": drivers[0].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "WB-01-CD-5678",
            "capacity": 12.0,
            "chassis_no": "CH23456789012345678",
            "engine_no": "EN23456789012345678",
            "owner_id": owners[1].id,
            "driver_id": drivers[1].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "KA-01-EF-9012",
            "capacity": 7.5,
            "chassis_no": "CH34567890123456789",
            "engine_no": "EN34567890123456789",
            "owner_id": owners[2].id,
            "driver_id": drivers[2].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "TN-01-GH-3456",
            "capacity": 10.0,
            "chassis_no": "CH45678901234567890",
            "engine_no": "EN45678901234567890",
            "owner_id": owners[3].id,
            "driver_id": drivers[3].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "DL-01-IJ-7890",
            "capacity": 8.5,
            "chassis_no": "CH56789012345678901",
            "engine_no": "EN56789012345678901",
            "owner_id": owners[4].id,
            "driver_id": drivers[4].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "GJ-01-KL-2345",
            "capacity": 11.0,
            "chassis_no": "CH67890123456789012",
            "engine_no": "EN67890123456789012",
            "owner_id": owners[5].id,
            "driver_id": drivers[5].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "TS-01-MN-6789",
            "capacity": 9.5,
            "chassis_no": "CH78901234567890123",
            "engine_no": "EN78901234567890123",
            "owner_id": owners[6].id,
            "driver_id": drivers[6].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "MH-12-OP-0123",
            "capacity": 8.0,
            "chassis_no": "CH89012345678901234",
            "engine_no": "EN89012345678901234",
            "owner_id": owners[7].id,
            "driver_id": drivers[7].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "RJ-01-QR-4567",
            "capacity": 10.5,
            "chassis_no": "CH90123456789012345",
            "engine_no": "EN90123456789012345",
            "owner_id": owners[8].id,
            "driver_id": drivers[8].id,
            "insurance_status": "ACTIVE"
        },
        {
            "lorry_no": "UP-32-ST-8901",
            "capacity": 7.0,
            "chassis_no": "CH01234567890123456",
            "engine_no": "EN01234567890123456",
            "owner_id": owners[9].id,
            "driver_id": drivers[9].id,
            "insurance_status": "ACTIVE"
        }
    ]
    
    vehicles = []
    for vehicle_data in vehicles_data:
        vehicle = Vehicle(**vehicle_data)
        db.session.add(vehicle)
        vehicles.append(vehicle)
    
    db.session.commit()
    print(f"✅ Created {len(vehicles)} vehicles")
    
    # 10. Create Concerned Persons
    print("👥 Creating concerned persons...")
    concerned_persons = []
    
    # Consignor concerned persons
    for i, consignor in enumerate(consignors):
        cp = ConcernedPerson(
            entity_type="CONSIGNOR",
            entity_id=consignor.id,
            name=f"Manager {i+1}",
            designation="Operations Manager",
            is_primary=True
        )
        db.session.add(cp)
        concerned_persons.append(cp)
    
    # Consignee concerned persons
    for i, consignee in enumerate(consignees):
        cp = ConcernedPerson(
            entity_type="CONSIGNEE",
            entity_id=consignee.id,
            name=f"Receiving Manager {i+1}",
            designation="Warehouse Manager",
            is_primary=True
        )
        db.session.add(cp)
        concerned_persons.append(cp)
    
    # Agent concerned persons
    for i, agent in enumerate(agents):
        cp = ConcernedPerson(
            entity_type="AGENT",
            entity_id=agent.id,
            name=f"Agent Manager {i+1}",
            designation="Booking Manager",
            is_primary=True
        )
        db.session.add(cp)
        concerned_persons.append(cp)
    
    # Driver concerned persons
    for i, driver in enumerate(drivers):
        cp = ConcernedPerson(
            entity_type="DRIVER",
            entity_id=driver.id,
            name=driver.name,
            designation="Driver",
            is_primary=True
        )
        db.session.add(cp)
        concerned_persons.append(cp)
    
    # Owner concerned persons
    for i, owner in enumerate(owners):
        cp = ConcernedPerson(
            entity_type="OWNER",
            entity_id=owner.id,
            name=owner.name,
            designation="Owner",
            is_primary=True
        )
        db.session.add(cp)
        concerned_persons.append(cp)
    
    db.session.commit()
    print(f"✅ Created {len(concerned_persons)} concerned persons")
    
    # 11. Create Phone Book entries
    print("📞 Creating phone book entries...")
    phone_books = []
    
    # Phone numbers for concerned persons
    for i, cp in enumerate(concerned_persons):
        phone = PhoneBook(
            concerned_person_id=cp.id,
            phone_number=f"+91-98765-{43200 + i}",
            is_primary=True,
            label="Mobile"
        )
        db.session.add(phone)
        phone_books.append(phone)
        
        # Add secondary phone numbers for some
        if i % 3 == 0:
            phone2 = PhoneBook(
                concerned_person_id=cp.id,
                phone_number=f"+91-22-{1234 + i}",
                is_primary=False,
                label="Office"
            )
            db.session.add(phone2)
            phone_books.append(phone2)
    
    db.session.commit()
    print(f"✅ Created {len(phone_books)} phone book entries")
    
    # 12. Create Orders
    print("📋 Creating orders...")
    orders = []
    
    # Create comprehensive orders with different scenarios
    order_scenarios = [
        # Recent orders (last 7 days) - NEW status
        {"days_ago": 1, "status": "NEW", "order_type": "PARTY", "description": "Urgent electronics shipment"},
        {"days_ago": 2, "status": "NEW", "order_type": "AGENT", "description": "Regular textile transport"},
        {"days_ago": 3, "status": "NEW", "order_type": "PARTY", "description": "Pharmaceutical delivery"},
        {"days_ago": 4, "status": "NEW", "order_type": "AGENT", "description": "Food and beverages transport"},
        {"days_ago": 5, "status": "NEW", "order_type": "PARTY", "description": "Construction materials"},
        
        # In progress orders (8-15 days ago)
        {"days_ago": 8, "status": "IN_PROGRESS", "order_type": "PARTY", "description": "Automotive parts shipment"},
        {"days_ago": 10, "status": "IN_PROGRESS", "order_type": "AGENT", "description": "Agricultural products"},
        {"days_ago": 12, "status": "IN_PROGRESS", "order_type": "PARTY", "description": "Machinery and equipment"},
        {"days_ago": 14, "status": "IN_PROGRESS", "order_type": "AGENT", "description": "Medical devices transport"},
        {"days_ago": 15, "status": "IN_PROGRESS", "order_type": "PARTY", "description": "Chemicals shipment"},
        
        # Completed orders (16-25 days ago)
        {"days_ago": 16, "status": "COMPLETED", "order_type": "PARTY", "description": "Furniture delivery"},
        {"days_ago": 18, "status": "COMPLETED", "order_type": "AGENT", "description": "Books and stationery"},
        {"days_ago": 20, "status": "COMPLETED", "order_type": "PARTY", "description": "Sports equipment"},
        {"days_ago": 22, "status": "COMPLETED", "order_type": "AGENT", "description": "Jewelry and accessories"},
        {"days_ago": 24, "status": "COMPLETED", "order_type": "PARTY", "description": "Paper and packaging"},
        
        # Cancelled orders
        {"days_ago": 6, "status": "CANCELLED", "order_type": "PARTY", "description": "Cancelled due to customer request"},
        {"days_ago": 11, "status": "CANCELLED", "order_type": "AGENT", "description": "Cancelled due to weather"},
        {"days_ago": 13, "status": "CANCELLED", "order_type": "PARTY", "description": "Cancelled due to vehicle breakdown"},
        
        # Additional orders for more variety
        {"days_ago": 7, "status": "NEW", "order_type": "AGENT", "description": "Rubber and plastic products"},
        {"days_ago": 9, "status": "IN_PROGRESS", "order_type": "PARTY", "description": "Metal products transport"},
        {"days_ago": 17, "status": "COMPLETED", "order_type": "AGENT", "description": "Glass and ceramics"},
        {"days_ago": 19, "status": "COMPLETED", "order_type": "PARTY", "description": "Leather products"},
        {"days_ago": 21, "status": "COMPLETED", "order_type": "AGENT", "description": "Cosmetics and personal care"},
        {"days_ago": 23, "status": "COMPLETED", "order_type": "PARTY", "description": "Textiles and garments"},
        {"days_ago": 25, "status": "COMPLETED", "order_type": "AGENT", "description": "Electronics and appliances"},
        {"days_ago": 26, "status": "COMPLETED", "order_type": "PARTY", "description": "Food and beverages"},
        {"days_ago": 28, "status": "COMPLETED", "order_type": "AGENT", "description": "Pharmaceuticals"},
        {"days_ago": 30, "status": "COMPLETED", "order_type": "PARTY", "description": "Automotive parts"},
    ]
    
    for i, scenario in enumerate(order_scenarios):
        order_date = date.today() - timedelta(days=scenario["days_ago"])
        order_type = scenario["order_type"]
        
        # Get random entities
        consignor = random.choice(consignors)
        consignee = random.choice(consignees)
        agent = random.choice(agents) if order_type == "AGENT" else None
        good = random.choice(goods)
        from_station = random.choice(stations)
        to_station = random.choice([s for s in stations if s.id != from_station.id])
        
        # Get concerned persons and phone numbers
        consignor_cp = next((cp for cp in concerned_persons if cp.entity_type == "CONSIGNOR" and cp.entity_id == consignor.id), None)
        consignee_cp = next((cp for cp in concerned_persons if cp.entity_type == "CONSIGNEE" and cp.entity_id == consignee.id), None)
        agent_cp = next((cp for cp in concerned_persons if cp.entity_type == "AGENT" and cp.entity_id == agent.id), None) if agent else None
        
        consignor_phone = next((pb for pb in phone_books if pb.concerned_person_id == consignor_cp.id and pb.is_primary), None) if consignor_cp else None
        consignee_phone = next((pb for pb in phone_books if pb.concerned_person_id == consignee_cp.id and pb.is_primary), None) if consignee_cp else None
        agent_phone = next((pb for pb in phone_books if pb.concerned_person_id == agent_cp.id and pb.is_primary), None) if agent_cp else None
        
        # Vary weight and rate based on status
        if scenario["status"] == "NEW":
            weight = random.uniform(1.0, 5.0)
            rate = random.uniform(50.0, 100.0)
        elif scenario["status"] == "IN_PROGRESS":
            weight = random.uniform(3.0, 10.0)
            rate = random.uniform(75.0, 150.0)
        elif scenario["status"] == "COMPLETED":
            weight = random.uniform(5.0, 15.0)
            rate = random.uniform(100.0, 200.0)
        else:  # CANCELLED
            weight = random.uniform(2.0, 8.0)
            rate = random.uniform(60.0, 120.0)
        
        order = Order(
            date=order_date,
            firm="New Jalaram Transport Service",
            order_type=order_type,
            from_station_id=from_station.id,
            to_station_id=to_station.id,
            station_pin_code=random.choice(pin_codes).code,
            consignor_id=consignor.id,
            consignee_id=consignee.id,
            booking_agent_id=agent.id if agent else None,
            consignor_concerned_person_id=consignor_cp.id if consignor_cp else None,
            consignor_phone_number_id=consignor_phone.id if consignor_phone else None,
            consignee_concerned_person_id=consignee_cp.id if consignee_cp else None,
            consignee_phone_number_id=consignee_phone.id if consignee_phone else None,
            agent_concerned_person_id=agent_cp.id if agent_cp else None,
            agent_phone_number_id=agent_phone.id if agent_phone else None,
            goods_id=good.id,
            weight=round(weight, 2),
            rate=round(rate, 2),
            description=scenario["description"],
            order_by=f"Customer {i+1}",
            party=f"Party {i+1}",
            status=scenario["status"]
        )
        db.session.add(order)
        orders.append(order)
    
    db.session.commit()
    print(f"✅ Created {len(orders)} orders")
    
    # 13. Create Builty records
    print("📄 Creating builty records...")
    builty_records = []
    
    # Create builty for orders with different status scenarios
    builty_scenarios = [
        # In Progress orders - IN_TRANSIT builty
        {"order_index": 5, "builty_status": "IN_TRANSIT", "days_after_order": 1, "description": "Vehicle dispatched"},
        {"order_index": 6, "builty_status": "IN_TRANSIT", "days_after_order": 2, "description": "In transit to destination"},
        {"order_index": 7, "builty_status": "IN_TRANSIT", "days_after_order": 1, "description": "On the way"},
        {"order_index": 8, "builty_status": "IN_TRANSIT", "days_after_order": 3, "description": "En route"},
        {"order_index": 9, "builty_status": "IN_TRANSIT", "days_after_order": 2, "description": "Transporting goods"},
        
        # Completed orders - DELIVERED builty
        {"order_index": 10, "builty_status": "DELIVERED", "days_after_order": 5, "description": "Successfully delivered"},
        {"order_index": 11, "builty_status": "DELIVERED", "days_after_order": 4, "description": "Delivery completed"},
        {"order_index": 12, "builty_status": "DELIVERED", "days_after_order": 6, "description": "Goods delivered"},
        {"order_index": 13, "builty_status": "DELIVERED", "days_after_order": 3, "description": "Delivery successful"},
        {"order_index": 14, "builty_status": "DELIVERED", "days_after_order": 7, "description": "Completed delivery"},
        {"order_index": 15, "builty_status": "DELIVERED", "days_after_order": 4, "description": "Delivered to consignee"},
        {"order_index": 16, "builty_status": "DELIVERED", "days_after_order": 5, "description": "Delivery completed"},
        {"order_index": 17, "builty_status": "DELIVERED", "days_after_order": 6, "description": "Successfully delivered"},
        {"order_index": 18, "builty_status": "DELIVERED", "days_after_order": 3, "description": "Delivery done"},
        {"order_index": 19, "builty_status": "DELIVERED", "days_after_order": 4, "description": "Completed"},
        
        # Some pending builty
        {"order_index": 0, "builty_status": "PENDING", "days_after_order": 0, "description": "Awaiting vehicle assignment"},
        {"order_index": 1, "builty_status": "PENDING", "days_after_order": 0, "description": "Pending driver assignment"},
        {"order_index": 2, "builty_status": "PENDING", "days_after_order": 0, "description": "Waiting for vehicle"},
    ]
    
    for i, scenario in enumerate(builty_scenarios):
        order = orders[scenario["order_index"]]
        vehicle = random.choice(vehicles)
        driver = vehicle.driver
        owner = vehicle.owner
        
        # Get concerned persons for driver and owner
        driver_cp = next((cp for cp in concerned_persons if cp.entity_type == "DRIVER" and cp.entity_id == driver.id), None)
        owner_cp = next((cp for cp in concerned_persons if cp.entity_type == "OWNER" and cp.entity_id == owner.id), None)
        
        driver_phone = next((pb for pb in phone_books if pb.concerned_person_id == driver_cp.id and pb.is_primary), None) if driver_cp else None
        owner_phone = next((pb for pb in phone_books if pb.concerned_person_id == owner_cp.id and pb.is_primary), None) if owner_cp else None
        
        # Calculate builty date
        builty_date = order.date + timedelta(days=scenario["days_after_order"])
        
        # Vary actual weight based on status
        if scenario["builty_status"] == "DELIVERED":
            actual_weight = order.weight + random.uniform(-0.2, 0.2)  # Minimal variation for delivered
        elif scenario["builty_status"] == "IN_TRANSIT":
            actual_weight = order.weight + random.uniform(-0.5, 0.5)  # Some variation in transit
        else:  # PENDING
            actual_weight = order.weight  # No change for pending
        
        builty = Builty(
            order_id=order.id,
            vehicle_id=vehicle.id,
            driver_id=driver.id,
            owner_id=owner.id,
            date=builty_date,
            firm="New Jalaram Transport Service",
            lr_no=f"LR{1000 + i}",
            from_station_id=order.from_station_id,
            to_station_id=order.to_station_id,
            status=scenario["builty_status"],
            invoice_no=f"INV{2000 + i}" if scenario["builty_status"] != "PENDING" else None,
            eway_bill_no=f"EWB{3000 + i}" if scenario["builty_status"] != "PENDING" else None,
            goods_id=order.goods_id,
            actual_weight=round(actual_weight, 2),
            charged_weight=order.weight,
            rate=order.rate,
            advance_amount=random.uniform(1000.0, 5000.0) if scenario["builty_status"] != "PENDING" else 0.0,
            consignor_id=order.consignor_id,
            consignee_id=order.consignee_id,
            booking_agent_id=order.booking_agent_id,
            consignor_concerned_person_id=order.consignor_concerned_person_id,
            consignor_phone_number_id=order.consignor_phone_number_id,
            consignee_concerned_person_id=order.consignee_concerned_person_id,
            consignee_phone_number_id=order.consignee_phone_number_id,
            agent_concerned_person_id=order.agent_concerned_person_id,
            agent_phone_number_id=order.agent_phone_number_id
        )
        db.session.add(builty)
        builty_records.append(builty)
    
    db.session.commit()
    print(f"✅ Created {len(builty_records)} builty records")
    
    # 14. Create Transaction Logs
    print("📊 Creating transaction logs...")
    transaction_logs = []
    
    # Create comprehensive transaction logs showing status updates and interactions
    for order in orders:
        # Order creation log
        log = TransactionLog(
            entity="Order",
            entity_id=order.id,
            action="CREATED",
            note=f"Order created for {order.consignor.name} to {order.consignee.name}",
            at=order.created_at
        )
        db.session.add(log)
        transaction_logs.append(log)
        
        # Status update logs based on order status
        if order.status == "IN_PROGRESS":
            # Order moved to in progress
            progress_log = TransactionLog(
                entity="Order",
                entity_id=order.id,
                action="STATUS_UPDATED",
                note=f"Order status updated to IN_PROGRESS - Vehicle assigned",
                at=order.created_at + timedelta(hours=2)
            )
            db.session.add(progress_log)
            transaction_logs.append(progress_log)
            
        elif order.status == "COMPLETED":
            # Order completed with multiple status updates
            progress_log = TransactionLog(
                entity="Order",
                entity_id=order.id,
                action="STATUS_UPDATED",
                note=f"Order status updated to IN_PROGRESS - Vehicle dispatched",
                at=order.created_at + timedelta(hours=1)
            )
            db.session.add(progress_log)
            transaction_logs.append(progress_log)
            
            completed_log = TransactionLog(
                entity="Order",
                entity_id=order.id,
                action="STATUS_UPDATED",
                note=f"Order status updated to COMPLETED - Delivery successful",
                at=order.created_at + timedelta(days=3)
            )
            db.session.add(completed_log)
            transaction_logs.append(completed_log)
            
        elif order.status == "CANCELLED":
            # Order cancelled
            cancel_log = TransactionLog(
                entity="Order",
                entity_id=order.id,
                action="STATUS_UPDATED",
                note=f"Order status updated to CANCELLED - {order.description}",
                at=order.created_at + timedelta(hours=4)
            )
            db.session.add(cancel_log)
            transaction_logs.append(cancel_log)
    
    # Create logs for builty with status transitions
    for builty in builty_records:
        # Builty creation log
        log = TransactionLog(
            entity="Builty",
            entity_id=builty.id,
            action="CREATED",
            note=f"Builty created for order {builty.order_id} - Vehicle {builty.vehicle.lorry_no}",
            at=builty.created_at
        )
        db.session.add(log)
        transaction_logs.append(log)
        
        # Status-specific logs
        if builty.status == "IN_TRANSIT":
            transit_log = TransactionLog(
                entity="Builty",
                entity_id=builty.id,
                action="STATUS_UPDATED",
                note=f"Builty status updated to IN_TRANSIT - Vehicle {builty.vehicle.lorry_no} dispatched",
                at=builty.created_at + timedelta(hours=1)
            )
            db.session.add(transit_log)
            transaction_logs.append(transit_log)
            
        elif builty.status == "DELIVERED":
            # Multiple status updates for delivered builty
            transit_log = TransactionLog(
                entity="Builty",
                entity_id=builty.id,
                action="STATUS_UPDATED",
                note=f"Builty status updated to IN_TRANSIT - Vehicle {builty.vehicle.lorry_no} dispatched",
                at=builty.created_at + timedelta(hours=1)
            )
            db.session.add(transit_log)
            transaction_logs.append(transit_log)
            
            delivered_log = TransactionLog(
                entity="Builty",
                entity_id=builty.id,
                action="STATUS_UPDATED",
                note=f"Builty status updated to DELIVERED - Goods delivered successfully",
                at=builty.created_at + timedelta(days=2)
            )
            db.session.add(delivered_log)
            transaction_logs.append(delivered_log)
            
        elif builty.status == "PENDING":
            pending_log = TransactionLog(
                entity="Builty",
                entity_id=builty.id,
                action="STATUS_UPDATED",
                note=f"Builty status set to PENDING - Awaiting vehicle assignment",
                at=builty.created_at + timedelta(minutes=30)
            )
            db.session.add(pending_log)
            transaction_logs.append(pending_log)
    
    # Create entity interaction logs
    for consignor in consignors[:3]:  # Log interactions for first 3 consignors
        interaction_log = TransactionLog(
            entity="Consignor",
            entity_id=consignor.id,
            action="UPDATED",
            note=f"Consignor {consignor.name} profile updated - Contact information refreshed",
            at=consignor.created_at + timedelta(days=5)
        )
        db.session.add(interaction_log)
        transaction_logs.append(interaction_log)
    
    for vehicle in vehicles[:3]:  # Log interactions for first 3 vehicles
        vehicle_log = TransactionLog(
            entity="Vehicle",
            entity_id=vehicle.id,
            action="UPDATED",
            note=f"Vehicle {vehicle.lorry_no} insurance status verified - Active",
            at=vehicle.created_at + timedelta(days=10)
        )
        db.session.add(vehicle_log)
        transaction_logs.append(vehicle_log)
    
    db.session.commit()
    print(f"✅ Created {len(transaction_logs)} transaction logs")
    
    print("\n🎉 Enhanced sample data creation completed successfully!")
    print(f"📊 Comprehensive Summary:")
    print(f"   • Stations: {len(stations)} (20 major Indian railway stations)")
    print(f"   • Pin Codes: {len(pin_codes)} (50+ realistic pin codes)")
    print(f"   • Goods: {len(goods)} (20 diverse categories)")
    print(f"   • Consignors: {len(consignors)} (10 major companies)")
    print(f"   • Consignees: {len(consignees)} (10 retail/e-commerce companies)")
    print(f"   • Booking Agents: {len(agents)} (10 logistics companies)")
    print(f"   • Owners: {len(owners)} (10 vehicle owners)")
    print(f"   • Drivers: {len(drivers)} (10 professional drivers)")
    print(f"   • Vehicles: {len(vehicles)} (10 commercial vehicles)")
    print(f"   • Concerned Persons: {len(concerned_persons)} (contact persons)")
    print(f"   • Phone Book Entries: {len(phone_books)} (comprehensive contacts)")
    print(f"   • Orders: {len(orders)} (25 orders with status variety)")
    print(f"   • Builty Records: {len(builty_records)} (18 delivery receipts)")
    print(f"   • Transaction Logs: {len(transaction_logs)} (comprehensive audit trail)")
    print(f"\n🔄 Status Distribution:")
    print(f"   • NEW Orders: {len([o for o in orders if o.status == 'NEW'])}")
    print(f"   • IN_PROGRESS Orders: {len([o for o in orders if o.status == 'IN_PROGRESS'])}")
    print(f"   • COMPLETED Orders: {len([o for o in orders if o.status == 'COMPLETED'])}")
    print(f"   • CANCELLED Orders: {len([o for o in orders if o.status == 'CANCELLED'])}")
    print(f"   • IN_TRANSIT Builty: {len([b for b in builty_records if b.status == 'IN_TRANSIT'])}")
    print(f"   • DELIVERED Builty: {len([b for b in builty_records if b.status == 'DELIVERED'])}")
    print(f"   • PENDING Builty: {len([b for b in builty_records if b.status == 'PENDING'])}")
    print(f"\n🎯 This data demonstrates:")
    print(f"   • Complete order-to-delivery workflows")
    print(f"   • Status transitions and interactions")
    print(f"   • Entity relationships and dependencies")
    print(f"   • Realistic business scenarios")
    print(f"   • Comprehensive audit trails")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_sample_data()
