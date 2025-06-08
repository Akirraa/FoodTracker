from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    
    path('recipes/', views.recipe_page, name='recipe_page'),  
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),

    path('api/recipes/', views.RecipeListAPI.as_view(), name='recipes_api'),
    path('recipes/create/', views.create_recipe, name='create_recipe'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)