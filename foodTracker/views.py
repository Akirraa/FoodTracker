from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests
import json
from datetime import date


from .models import Recipe, Food
from .serializers import FoodSerializer, FoodLogSerializer
from .models import Food_Log
from rest_framework import viewsets, permissions
from django.utils.dateparse import parse_date



@csrf_exempt
@require_POST
def test_api(request):
    print("test_api called")
    return JsonResponse({"message": "Test API reached"})


# HuggingFace API config
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
}

def query_huggingface(prompt):
    try:
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=15
        )

        if response.status_code != 200:
            return None, f"Model API error: {response.status_code} - {response.text}"

        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"], None
        return None, "Unexpected response format from Hugging Face API."

    except requests.RequestException as e:
        return None, f"Request failed: {str(e)}"


@csrf_exempt
def generate_nutrition_tips_rule_based(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        body = json.loads(request.body)
        nutrition = body.get("nutrition")
        if not nutrition:
            return JsonResponse({"error": "Missing 'nutrition' field"}, status=400)

        calories = nutrition.get("calories", 0)
        protein = nutrition.get("protein", 0)
        carbs = nutrition.get("carbs", 0)
        fats = nutrition.get("fats", 0)
        fiber = nutrition.get("fiber", 0)
        sugar = nutrition.get("sugar", 0)
        cholesterol = nutrition.get("cholesterol", 0)
        sodium = nutrition.get("sodium", 0)
        calcium = nutrition.get("calcium", 0)
        iron = nutrition.get("iron", 0)
        potassium = nutrition.get("potassium", 0)

        tips = []

        # Calories
        if calories < 1800:
            tips.append("Eat nutrient-dense snacks to boost calories.")
        elif calories > 2800:
            tips.append("Reduce portion sizes to manage calories.")
        else:
            tips.append("Calorie intake is balanced.")

        # Protein
        if protein < 50:
            tips.append("Add lean meats, beans, or dairy for protein.")
        elif protein > 150:
            tips.append("Drink more water and balance meals.")
        else:
            tips.append("Protein intake looks good.")

        # Carbs
        if carbs < 130:
            tips.append("Include whole grains and fruits for energy.")
        elif carbs > 300:
            tips.append("Balance carbs with protein and healthy fats.")
        else:
            tips.append("Carb intake is healthy.")

        # Fats
        if fats < 20:
            tips.append("Eat avocados, nuts, or olive oil for fats.")
        elif fats > 80:
            tips.append("Choose unsaturated fats; limit saturated fats.")
        else:
            tips.append("Fat intake is healthy.")

        # Fiber
        if fiber and fiber < 25:
            tips.append("Add veggies, fruits, and whole grains for fiber.")
        elif fiber:
            tips.append("Fiber intake is good.")

        # Sugar
        if sugar > 50:
            tips.append("Cut back on sugary drinks and snacks.")

        # Cholesterol
        if cholesterol > 300:
            tips.append("Limit saturated fats and processed foods.")

        # Sodium
        if sodium > 2300:
            tips.append("Reduce salt to control blood pressure.")

        # Calcium
        if calcium < 1000:
            tips.append("Eat dairy or fortified plant alternatives.")
        else:
            tips.append("Calcium intake supports strong bones.")

        # Iron
        if iron < 8:
            tips.append("Add leafy greens, beans, or lean meats.")
        else:
            tips.append("Iron levels look good.")

        # Potassium
        if potassium < 3500:
            tips.append("Eat more bananas, oranges, and spinach.")

        # Hydration reminder
        tips.append("Stay hydrated with plenty of water.")

        # Remove duplicates, keep first 5 tips only
        seen = set()
        unique_tips = []
        for tip in tips:
            if tip not in seen:
                unique_tips.append(tip)
                seen.add(tip)
            if len(unique_tips) >= 3:
                break

        return JsonResponse({"tips": unique_tips})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# Home page view
def home(request):
    return render(request, 'FoodTracker/home.html', {'dark_bg': True})


# Search suggestions for recipes and foods
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


# Recipe detail page
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'FoodTracker/recipe_details.html', {'recipe': recipe})


# Food detail page
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'FoodTracker/food_details.html', {'food': food})


# About us page
def about_us(request):
    return render(request, 'FoodTracker/about_us.html', {'dark_bg': False})


# API endpoint for listing foods
@api_view(['GET'])
def food_list(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)


# Tracking page view
def tracking_page(request):
    return render(request, 'FoodTracker/tracking.html', {'dark_bg': True})



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

from rest_framework.response import Response
@csrf_exempt
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def save_selected_foods(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_foods = data.get('foods', [])
            nutrition_totals = data.get('nutritionTotals', {})

            if not selected_foods:
                return JsonResponse({'status': 'error', 'message': 'No foods provided'}, status=400)

            user = request.user
            today = now().date()

            saved_count = 0
            for item in selected_foods:
                food_id = item.get('id')
                quantity = float(item.get('quantity', 1.0))

                if not food_id:
                    continue

                try:
                    food = Food.objects.get(id=food_id)
                except Food.DoesNotExist:
                    continue

                # Check if a log already exists for this user-food-date combo
                food_log, created = Food_Log.objects.update_or_create(
                    user=user,
                    food=food,
                    date=today,
                    quantity=quantity,
                    nutritions=nutrition_totals,  # Store nutrition details as JSON
                )

                saved_count += 1

            return JsonResponse({'status': 'success', 'saved': saved_count, 'nutrition': nutrition_totals})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)



from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Recipe
from .serializers import RecipeSerializer
from .forms import RecipeForm, RecipeIngredientFormSet
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


class RecipePagination(PageNumberPagination):
    page_size = 6

class RecipeListAPI(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    
    
    
def recipe_page(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)  # 6 recipes per page

    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    return render(request, "recipes/recipes.html", {
        'dark_bg': True,
        'page_obj': page_obj,
    })
    
    
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe  # Bind formset to the saved recipe
            formset.save()
            return redirect('recipe_page')  # Change to your success URL

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {
        'form': form,
        'formset': formset,
        'dark_bg': True,  # Assuming you want a dark background for this page
    }
    return render(request, 'recipes/create_recipe.html', context)

from django.shortcuts import get_object_or_404, render
from .models import Recipe

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    instruction_lines = [line.strip() for line in recipe.instructions.strip().splitlines() if line.strip()]
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'instruction_lines': instruction_lines,
        'dark_bg': True,
    })
