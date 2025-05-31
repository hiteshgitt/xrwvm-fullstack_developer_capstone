from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    
    # Root level URLs
    path('login/', views.login_user, name='login'),
    path('api/login/', views.login_api, name='login_api'),
    path('register/', views.registration, name='register'),  # Add this line
    
    # Add other root level URLs as needed
    path('about/', views.about_view, name='about'),  # You'll need to create this view
    path('contact/', views.contact_view, name='contact'),  # You'll need to create this view
    
    # Default root path
    path('', views.home_view, name='home'),  # You'll need to create this view
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)