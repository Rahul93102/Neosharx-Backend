# Neosharx-Backend

A comprehensive Django REST API backend for the Neosharx platform, featuring user authentication, content management, and social features.

## 🚀 Features

- **User Authentication**: JWT-based auth with Google and LinkedIn OAuth
- **Content Management**: Events, hackathons, startups, robotics news, tech news
- **Social Features**: Comments system, user profiles, admin panel
- **API**: RESTful API with Django REST Framework
- **Database**: PostgreSQL for production, SQLite for development
- **Deployment**: Ready for Render deployment with automated CI/CD

## 🛠️ Tech Stack

- **Backend**: Django 5.1.7 + Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT, Google OAuth, LinkedIn OAuth
- **SMS**: Twilio integration
- **Deployment**: Render (with render.yaml blueprint)

## 📋 Prerequisites

- Python 3.11.9
- PostgreSQL (for production)
- GitHub repository
- OAuth apps (Google, LinkedIn)
- Twilio account

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rahul93102/Neosharx-Backend.git
   cd Neosharx-Backend
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   python create_admin.py
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Frontend domains for CORS
- OAuth credentials for Google and LinkedIn
- Twilio credentials for SMS

### OAuth Setup

1. **Google OAuth**:
   - Create project at [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Set redirect URI: `https://yourdomain.com/auth/google/callback.html`

2. **LinkedIn OAuth**:
   - Create app at [LinkedIn Developers](https://developer.linkedin.com/)
   - Set redirect URI: `https://yourdomain.com/auth/linkedin/callback.html`

## 🚀 Deployment

### Render Deployment

1. **Connect Repository**: Link your GitHub repo to Render
2. **Blueprint Deployment**: Use `render.yaml` for automated setup
3. **Environment Variables**: Configure OAuth and Twilio credentials
4. **Database**: PostgreSQL will be auto-provisioned

### Manual Deployment

```bash
# Install production dependencies
pip install -r requirements_prod.txt

# Run migrations
python manage_prod.py migrate

# Start server
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/google/login-url/` - Google OAuth URL
- `GET /api/auth/linkedin/login-url/` - LinkedIn OAuth URL

### Content Endpoints
- `GET /api/events/` - List events
- `GET /api/hackathons/` - List hackathons
- `GET /api/startups/` - List startup stories
- `GET /api/robotics-news/` - Robotics news
- `GET /api/tech-news/` - Tech news

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test authentication.tests

# Test API endpoints
python test_api.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support, please contact the development team or create an issue in the repository.
