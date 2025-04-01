from django.db import models

# Create your models here.
class Person(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class meta:
        abstract = True
    
    def __str__(self):
        return self.Username
    

class user(Person):
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    
    class meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["Username"]
        

class food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    fiber = models.FloatField()
    serving_size = models.CharField(max_length=20)
    
    
    class meta:
        db_table = "food"
        verbose_name = "food"
        verbose_name_plural = "foods"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    

class food_log(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class meta:
        db_table = "food_log"
        verbose_name = "food_log"
        verbose_name_plural = "food_logs"
        ordering = ["date"]
    
    def __str__(self):
        return f"{self.user.Username} - {self.food.name} - {self.date}"    
    

class recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    
    class meta:
        db_table = "recipe"
        verbose_name = "recipe"
        verbose_name_plural = "recipes"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
class recipe_ingredient(models.Model):
    recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    quantity = models.FloatField()
    
    class meta:
        db_table = "recipe_ingredient"
        verbose_name = "recipe_ingredient"
        verbose_name_plural = "recipe_ingredients"
        ordering = ["recipe"]
        
    def __str__(self):
        return f"{self.recipe.name} - {self.food.name} - {self.quantity}"