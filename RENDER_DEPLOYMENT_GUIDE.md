# 🚀 Render Deployment Guide for Neosharx Backend

## 📋 Prerequisites

- GitHub repository connected to Render
- OAuth apps configured (LinkedIn, Google)
- Twilio account set up

## 🔧 Configuration Files Created/Updated

### 1. render.yaml (Blueprint Deployment)

```yaml
services:
  - type: web
    name: neosharx-backend
    runtime: python3
    buildCommand: pip install -r requirements_prod.txt && python manage_prod.py migrate
    startCommand: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3
    envVars:
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          type: postgresql
          name: neosharx-db
          property: connectionString
      - key: ALLOWED_HOSTS
        fromService:
          type: web
          name: neosharx-backend
          property: host
      - key: CORS_ALLOWED_ORIGINS
        value: https://your-frontend-domain.com,https://www.your-frontend-domain.com
      - key: LINKEDIN_CLIENT_ID
        sync: false
      - key: LINKEDIN_CLIENT_SECRET
        sync: false
      - key: GOOGLE_CLIENT_ID
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: TWILIO_VERIFY_SERVICE_SID
        sync: false

databases:
  - name: neosharx-db
    databaseName: neosharx_db
    user: neosharx_user
```

### 2. Updated .env File

```bash
# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID=your_linkedin_client_id_here
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_VERIFY_SERVICE_SID=your_twilio_verify_service_sid_here

# Django Production Settings
SECRET_KEY=django-insecure-production-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-render-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
CORS_ALLOW_ALL_ORIGINS=False

# Database (Leave empty for Render - it will be set automatically)
DATABASE_URL=
```

## 🚀 Deployment Steps

### Option 1: Blueprint Deployment (Recommended)

1. **Connect Repository**: Go to Render.com and connect your GitHub repository
2. **Create Blueprint**: Upload the `render.yaml` file or use the content above
3. **Configure Environment Variables**: The blueprint will prompt for sensitive values
4. **Deploy**: Click "Apply" to deploy the entire stack

### Option 2: Manual Deployment

1. **Create Web Service**:

   - Runtime: Python 3
   - Build Command: `pip install -r requirements_prod.txt && python manage_prod.py migrate`
   - Start Command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3`

2. **Create PostgreSQL Database**:

   - Add a PostgreSQL database in Render
   - Link it to your web service

3. **Set Environment Variables**:
   ```
   DEBUG=False
   SECRET_KEY=your-unique-secret-key-here
   DATABASE_URL=postgresql://... (provided by Render)
   ALLOWED_HOSTS=your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   LINKEDIN_CLIENT_ID=your_linkedin_client_id_here
   LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_VERIFY_SERVICE_SID=your_twilio_verify_service_sid_here
   ```

## 🔄 Post-Deployment Configuration

### Update OAuth Redirect URIs

After deployment, update your OAuth app settings:

**LinkedIn App**:

- Redirect URI: `https://your-app-name.onrender.com/auth/linkedin/callback.html`

**Google OAuth App**:

- Redirect URI: `https://your-app-name.onrender.com/auth/google/callback.html`

### Update CORS Origins

Update `CORS_ALLOWED_ORIGINS` in Render environment variables with your actual frontend domain.

## ✅ Verification Steps

1. **Check Application Logs**: Monitor Render logs for any startup errors
2. **Test Database Connection**: Verify migrations ran successfully
3. **Test API Endpoints**:
   ```bash
   curl https://your-app-name.onrender.com/api/health/
   ```
4. **Test Authentication**: Try OAuth flows with updated redirect URIs

## 🔧 Troubleshooting

### Common Issues:

- **Database Connection**: Ensure DATABASE_URL is set correctly
- **Static Files**: WhiteNoise should handle static files automatically
- **CORS Errors**: Update CORS_ALLOWED_ORIGINS with correct frontend URL
- **OAuth Redirects**: Ensure redirect URIs match deployed domain

### Environment Variables:

- Never commit secrets to git
- Use Render's environment variable management
- Generate a new SECRET_KEY for production

## 📊 Performance Optimization

- **Workers**: Gunicorn configured with 3 workers for basic load
- **Database**: PostgreSQL provides better performance than SQLite
- **Static Files**: WhiteNoise serves static files efficiently
- **Caching**: Consider adding Redis for session caching in future

## 🔒 Security Checklist

- ✅ SECRET_KEY generated uniquely for production
- ✅ DEBUG=False in production
- ✅ ALLOWED_HOSTS configured
- ✅ HTTPS enabled by default on Render
- ✅ Database credentials not in code
- ✅ OAuth secrets in environment variables
- ✅ CORS properly configured

---

🎉 **Your Neosharx backend is now fully deployment-ready for Render!**
