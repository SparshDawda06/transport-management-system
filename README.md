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

4. **Access the Application**:
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

## Development

The application is built with:
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **WTForms**: Form handling
- **Jinja2**: Template engine
- **SQLite**: Database