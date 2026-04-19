from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from .models import Category, Wish
from .serializers import CategorySerializer, WishSerializer

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

class WishViewSet(ModelViewSet):
    serializer_class = WishSerializer

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)