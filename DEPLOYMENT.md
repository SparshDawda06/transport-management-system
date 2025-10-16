# 🚀 Deployment Guide

Your Transport Management System is now ready for deployment! Here are several options to get it live:

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier Available)
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy
6. Your app will be live at `https://your-app-name.railway.app`

### Option 2: Heroku (Free Tier Discontinued, Paid Plans Available)
1. Install Heroku CLI: `brew install heroku/brew/heroku`
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git add . && git commit -m "Deploy" && git push heroku main`
5. Run migrations: `heroku run flask db upgrade`

### Option 3: DigitalOcean App Platform
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app → GitHub
3. Select your repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --bind 0.0.0.0:$PORT wsgi:application`
5. Deploy!

### Option 4: Render (Free Tier Available)
1. Go to [Render.com](https://render.com)
2. Connect GitHub account
3. Create "Web Service"
4. Select your repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT wsgi:application`
6. Deploy!

### Option 5: VPS Deployment (DigitalOcean Droplet, AWS EC2, etc.)
```bash
# On your server
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone your repo
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Install dependencies
pip3 install -r requirements.txt

# Run migrations
FLASK_APP=run.py python3 -m flask db upgrade

# Start with systemd service
sudo systemctl start your-app
sudo systemctl enable your-app
```

## 🔧 Environment Variables

Set these in your hosting platform:

- `SECRET_KEY`: A random secret key (generate with `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- `FLASK_ENV`: `production`
- `DATABASE_URL`: (Optional, defaults to SQLite)

## 📊 Default Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login!

## 🐳 Docker Deployment

```bash
# Build and run locally
docker build -t tms-app .
docker run -p 8000:8000 tms-app

# Push to Docker Hub
docker tag tms-app yourusername/tms-app
docker push yourusername/tms-app
```

## 🔍 Health Check

Your app includes a health check endpoint: `/health`

## 📱 Features Available

✅ User Authentication  
✅ Order Management  
✅ Fleet Management  
✅ Entity Management  
✅ Document Management  
✅ Phone Book  
✅ System Configuration  
✅ Responsive Design  

## 🆘 Troubleshooting

- **Port 5000 issues**: Use port 8000 instead (macOS AirPlay conflict)
- **Database errors**: Run `flask db upgrade` after deployment
- **Permission errors**: Ensure uploads directory exists and is writable

## 📞 Support

If you encounter issues, check the logs in your hosting platform's dashboard.
