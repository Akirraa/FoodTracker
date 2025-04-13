from django.shortcuts import render
from django.db.models import Q
from .models import Recipe, Food
from django.http import JsonResponse
# Create your views here.


# Home page
def home(request):
    
    return render(request, 'FoodTracker/home.html', {'dark_bg':True}) 




def search_suggestions(request): 
    query = request.GET.get('q', '').strip() 
    suggestions = []

    if query:
        # Recipes starting with query
        recipes = Recipe.objects.filter(name__istartswith=query).values('id', 'name')[:5]
        suggestions += [
            {
                'type': 'recipe',
                'name': r['name'],
                'url': f'/recipes/{r["id"]}/'
            }
            for r in recipes
        ]

        # Foods starting with query
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
