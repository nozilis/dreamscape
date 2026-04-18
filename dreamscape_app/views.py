from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Wish
from .serializers import CategorySerializer, WishSerializer

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class WishListView(APIView):
    def get(self, request):
        wishes = Wish.objects.filter(user=request.user).order_by('-created_at')
        serializer = WishSerializer(wishes, many=True)
        return Response(serializer.data)