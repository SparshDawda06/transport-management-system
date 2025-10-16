# Transport Management System (TMS)

A comprehensive Flask-based web application for managing transportation operations, built for modern deployment and scalability.

## 🚀 Live Demo

**The application is now live and ready to deploy!**

## ✨ Features

- **Order Management**: Create and manage transportation orders
- **Builty Management**: Handle delivery receipts and documentation
- **Entity Management**: Manage consignors, consignees, and booking agents
- **Fleet Management**: Track vehicles, drivers, and owners
- **System Configuration**: Manage stations, goods, and pin codes
- **Phone Book**: Comprehensive contact management system
- **User Authentication**: Secure login system with role-based access
- **Responsive Design**: Modern, mobile-friendly interface

## 🚀 Quick Start

### Option 1: Automated Deployment
```bash
# Run the deployment script
./deploy.sh
```

### Option 2: Manual Setup
1. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run Database Migrations**:
   ```bash
   FLASK_APP=run.py python3 -m flask db upgrade
   ```

3. **Start the Application**:
   ```bash
   # Development
   python3 run.py
   
   # Production
   gunicorn --bind 0.0.0.0:8000 wsgi:application
   ```

4. **Populate Sample Data** (Optional):
   ```bash
   # Quick way to add sample data
   python3 seed_sample_data.py
   
   # Or using Flask CLI
   FLASK_APP=run.py flask seed-data
   ```

5. **Access the Application**:
   - Open your browser and go to `http://localhost:8000`
   - Default login: `admin` / `admin123`

## 🌐 Deployment Options

### Heroku Deployment
1. Install Heroku CLI
2. Create a new Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`
4. Run migrations: `heroku run flask db upgrade`

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python app and deploy
3. Set environment variables in Railway dashboard

### DigitalOcean App Platform
1. Connect your repository
2. Configure build command: `pip install -r requirements.txt`
3. Configure run command: `gunicorn --bind 0.0.0.0:$PORT wsgi:application`

### Docker Deployment
```bash
# Build the image
docker build -t tms-app .

# Run the container
docker run -p 8000:8000 tms-app
```

## Project Structure

```
app/
├── __init__.py          # Application factory
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms.py            # WTForms definitions
├── auth.py             # Authentication logic
├── extensions.py       # Flask extensions
├── blueprints/         # Blueprint modules
│   ├── orders.py       # Order management
│   ├── builty.py       # Builty management
│   ├── entities.py     # Consignors, consignees, agents
│   ├── fleet.py        # Vehicles, drivers, owners
│   ├── system.py       # Stations, goods, pin codes
│   ├── phonebook.py    # Phone book management
│   └── auth.py         # Authentication routes
├── templates/          # Jinja2 templates
│   ├── entities/       # Entity management templates
│   ├── fleet/          # Fleet management templates
│   └── system/         # System configuration templates
├── static/            # Static files (CSS, JS)
└── main/              # Main application routes
```

## Database

The application uses SQLite database by default. The database file will be created automatically in the `instance/` directory.

## 📊 Enhanced Sample Data

The application includes comprehensive sample data with status interactions:

- **Stations**: 20 major Indian railway stations across multiple states
- **Pin Codes**: 50+ realistic pin codes linked to stations  
- **Goods**: 20 diverse transportation categories
- **Consignors**: 10 major companies (Reliance, Tata, Infosys, Wipro, HUL, etc.)
- **Consignees**: 10 retail/e-commerce companies (Amazon, Flipkart, BigBasket, etc.)
- **Booking Agents**: 10 logistics companies across different cities
- **Fleet**: 10 vehicles with owners and drivers
- **Orders**: 25 sample orders with status variety (NEW, IN_PROGRESS, COMPLETED, CANCELLED)
- **Builty**: 18 delivery receipts with status interactions (IN_TRANSIT, DELIVERED, PENDING)
- **Phone Book**: Complete contact management system
- **Transaction Logs**: 100+ comprehensive audit trail entries

**Status Interactions Demonstrated:**
- Complete order-to-delivery workflows
- Status transitions and entity interactions
- Realistic business scenarios with audit trails
- Entity relationships and dependencies

See [SAMPLE_DATA.md](SAMPLE_DATA.md) for detailed information about the enhanced sample data.

## Development

The application is built with:
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **WTForms**: Form handling
- **Jinja2**: Template engine
- **SQLite**: Database