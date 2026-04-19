from rest_framework import serializers
from .models import User, Category, Wish

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class WishSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Wish
        fields = ['title', 'description', 'last_wish_at', 'images', 'is_done', 'location', 'gift_url', 'category']