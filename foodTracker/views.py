from django.shortcuts import render, redirect
from django.db.models import Q #hedi bch t7adharlk querry bch na3ml search lel recipes w foods fil home page
from .models import Recipe, Food #hedhom lmodels mte3i xd
from django.http import JsonResponse #hedhi bch na3mlou ajax call lel search bar
from .serializers import FoodSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import json

# Create your views here.


# Home page
def home(request):
    
    return render(request, 'FoodTracker/home.html', {'dark_bg':True}) 


def search_suggestions(request): 
    query = request.GET.get('q', '').strip() 
    suggestions = []

    if query:
        recipes = Recipe.objects.filter(name__istartswith=query).values('id', 'name')[:5]
        suggestions += [
            {
                'type': 'recipe',
                'name': r['name'],
                'url': f'/recipes/{r["id"]}/'
            }
            for r in recipes
        ]

        foods = Food.objects.filter(name__istartswith=query).values('id', 'name')[:5]
        suggestions += [
            {
                'type': 'food',
                'name': f['name'],
                'url': f'/foods/{f["id"]}/'
            }
            for f in foods
        ]

    return JsonResponse({'results': suggestions})


def recipe_detail(request, pk):
    r = Recipe.objects.get(pk=pk)
    return render(request, 'FoodTracker/recipe_detail.html', {'recipe': r})

def food_detail(request, pk):
    f = Food.objects.get(pk=pk)
    return render(request, 'FoodTracker/food_detail.html', {'food': f})


def about_us(request):
    return render(request, 'FoodTracker/about_us.html', {'dark_bg': False})

@api_view(['GET'])
def food_list(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


def tracking_page(request):
    return render(request, 'FoodTracker/tracking.html', {'dark_bg': True})
