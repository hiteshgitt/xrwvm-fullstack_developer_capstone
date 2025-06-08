from django.urls import path
from . import views

urlpatterns = [
    # Login URLs
    path('login/', views.login_user, name='login'),
    path('login_api/', views.login_api, name='login_api'),
    
    # Car-related URLs
    path(route='get_cars', view=views.get_cars, name='getcars'),
    
    # Comment out any URLs that reference non-existent views
    # path('reviews/', views.review_list, name='review_list'),
    
    # Add other URLs as you implement the corresponding views
    path('logout/', views.logout_api, name='logout_api'),
    # path('register/', views.registration, name='registration'),
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path('add_review/', views.add_review, name='add_review'),
]