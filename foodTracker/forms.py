from django import forms
from .models import Recipe, Recipe_Ingredient
from django.forms import inlineformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'prep_time', 'cook_time', 'servings', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = Recipe_Ingredient
        fields = ['food', 'quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'placeholder': 'e.g., 2 cups, 100g'}),
        }

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    Recipe_Ingredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)
