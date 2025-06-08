from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('foods/<int:pk>/', views.food_detail, name='food_detail'),
    path('tracking/', views.tracking_page, name='tracking_page'),

    # About us page 
    path('about-us/', views.about_us, name='about_us'),

    # API endpoints
    path('api/foods/', views.food_list, name='food-list'),
    path('api/generate-tip/', views.generate_nutrition_tips_rule_based, name='generate_nutrition_tips'),
    
    path('api/save-selected-foods/', views.save_selected_foods, name='save_selected_foods'),

]
