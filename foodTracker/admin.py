from django.contrib import admin
from .models import  Food, Food_Log, Recipe, Recipe_Ingredient



# Register your models here.
admin.site.site_header = "Nutra Admin Panel"
admin.site.site_title = "Nutra Admin Panel"
admin.site.index_title = "Welcome to Nutra Admin Panel"
admin.site.empty_value_display = '**Empty**'



class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fats', 'fiber', 'sugar', 'water', 'sodium', 'calcium', 'iron', 'potassium', 'cholesterol')

    search_fields = ('name',)
    list_filter = (
        ('sodium'), 
        ('calcium'), 
        ('iron'), 
        ('potassium'),
    )  
    ordering = ('name',)


class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'date', 'created_at', 'updated_at')
    
    search_fields = ('user__username', 'food__name')
    list_filter = ('date',)
    ordering = ('-date',)
    
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'prep_time', 'cook_time', 'servings')
    
    search_fields = ('name',)
    ordering = ('name',)

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'food', 'quantity')
    
    search_fields = ('recipe__name', 'food__name')
    ordering = ('recipe',)


admin.site.register(Food, FoodAdmin)
admin.site.register(Food_Log, FoodLogAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Recipe_Ingredient, RecipeIngredientAdmin)