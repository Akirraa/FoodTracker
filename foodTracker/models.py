from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
class Person(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.Username
    

class user(Person):
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    
    class Meta:
        db_table = "user"
        ordering = ["Username"]
        

class food(models.Model):
    name = models.CharField(max_length=200)
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
    

class food_log(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "food_log"
        ordering = ["date"]
    
    def __str__(self):
        return f"{self.user.Username} - {self.food.name} - {self.date}"    
    

class recipe(models.Model):
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
    
class recipe_ingredient(models.Model):
    recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    
    class Meta:
        db_table = "recipe_ingredient"
        ordering = ["recipe"]
        
    def __str__(self):
        return f"{self.recipe.name} - {self.food.name} - {self.quantity}"