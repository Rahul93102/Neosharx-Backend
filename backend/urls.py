from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
import os

def serve_callback_file(request, provider):
    """Serve OAuth callback HTML files"""
    # BASE_DIR is /Users/vishaljha/neosharx/Backend flow
    # Frontend files are at /Users/vishaljha/neosharx/frontend/
    file_path = os.path.join(settings.BASE_DIR.parent, 'frontend', 'auth', provider, 'callback.html')
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(f"Callback file for {provider} not found at {file_path}", status=404)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    # OAuth callback file serving
    path("auth/google/callback.html", lambda request: serve_callback_file(request, 'google')),
    path("auth/linkedin/callback.html", lambda request: serve_callback_file(request, 'linkedin')),
]
