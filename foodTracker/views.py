from django.shortcuts import render
from django.db.models import Q
from .models import recipe, food
from django.http import JsonResponse
# Create your views here.


# Home page
def home(request):
    query = request.GET.get('q')
    if query:
        recipes_found = recipe.objects.filter(Q(name__icontains=query))
        foods_found = food.objects.filter(Q(name__icontains=query))
    else:
        recipes_found = []
        foods_found = []

    result ={  'recipes_found': recipes_found,
        'foods_found': foods_found,}
    return render(request, 'FoodTracker/home.html',result )




def search_suggestions(request): 
    query = request.GET.get('q', '').strip() 
    suggestions = []

    if query:
        # Recipes starting with query
        recipes = recipe.objects.filter(name__istartswith=query).values('id', 'name')[:5]
        suggestions += [
            {
                'type': 'recipe',
                'name': r['name'],
                'url': f'/recipes/{r["id"]}/'
            }
            for r in recipes
        ]

        # Foods starting with query
        foods = food.objects.filter(name__istartswith=query).values('id', 'name')[:5]
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
    r = recipe.objects.get(pk=pk)
    return render(request, 'FoodTracker/recipe_detail.html', {'recipe': r})

def food_detail(request, pk):
    f = food.objects.get(pk=pk)
    return render(request, 'FoodTracker/food_detail.html', {'food': f})

