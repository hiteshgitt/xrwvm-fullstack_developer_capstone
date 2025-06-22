from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from djangoapp import views
from django.views.generic import TemplateView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    
    # Root level URLs
    path('login/', views.login_user, name='login'),
    path('api/login/', views.login_api, name='login_api'),
    path('register/', views.registration, name='register'),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    
    # Add other root level URLs as needed
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Default root path
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add this line to serve static files from the React build directory
    urlpatterns += static('/static/', document_root=os.path.join(settings.BASE_DIR, 'frontend/build/static'))