from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.home, name='home'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('foods/<int:pk>/', views.food_detail, name='food_detail'),
    path('tracking/', views.tracking_page, name='tracking_page'),

    #about us page 
    path('about-us/', views.about_us, name='about_us'),
    
    
    #api endpoints
    path('api/foods/', views.food_list, name='food-list'),
]