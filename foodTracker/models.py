from django.db import models
from django.core.validators import MinValueValidator
from authentification.models import User

        

class Food(models.Model):
    name = models.CharField(max_length=200, default="")
    calories = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    protein = models.FloatField(default=0, validators=[MinValueValidator(0)])
    carbs = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fats = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fiber = models.FloatField(default=0, validators=[MinValueValidator(0)])
    sugar = models.FloatField(default=0, validators=[MinValueValidator(0)])
    water = models.FloatField(default=0, validators=[MinValueValidator(0)])
    sodium = models.FloatField(default=0, validators=[MinValueValidator(0)])
    calcium = models.FloatField(default=0, validators=[MinValueValidator(0)])
    iron = models.FloatField(default=0, validators=[MinValueValidator(0)])
    potassium = models.FloatField(default=0, validators=[MinValueValidator(0)])
    cholesterol = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = "food"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    

class Food_Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "food_log"
        ordering = ["date"]
    
    def __str__(self):
        return f"{self.user.Username} - {self.food.name} - {self.date}"    
    

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    
    class Meta:
        db_table = "recipe"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
class Recipe_Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    
    class Meta:
        db_table = "recipe_ingredient"
        ordering = ["recipe"]
        
    def __str__(self):
        return f"{self.recipe.name} - {self.food.name} - {self.quantity}"