from rest_framework import serializers
from .models import Food, Food_Log

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class FoodLogSerializer(serializers.ModelSerializer):
    food_details = FoodSerializer(source='food', read_only=True)
    total_calories = serializers.SerializerMethodField()
    total_protein = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    total_fats = serializers.SerializerMethodField()

    class Meta:
        model = Food_Log
        fields = [
            'id', 'user', 'food', 'food_details', 'quantity',
            'date', 'created_at', 'updated_at',
            'total_calories', 'total_protein', 'total_carbs', 'total_fats',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_calories(self, obj):
        return obj.total_calories()

    def get_total_protein(self, obj):
        return obj.total_protein()

    def get_total_carbs(self, obj):
        return obj.total_carbs()

    def get_total_fats(self, obj):
        return obj.total_fats()
