from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Wish
from .serializers import CategorySerializer, WishSerializer, RegisterSerializer
from .permissions import UserAccessPermission
from rest_framework import generics

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class WishViewSet(ModelViewSet):
    serializer_class = WishSerializer
    permission_classes = [IsAuthenticated, UserAccessPermission]

    def get_queryset(self):
        user_id = int(self.request.query_params.get('user_id', 0))
        if user_id == self.request.user.id:
            return Wish.objects.filter(user=self.request.user).order_by('-created_at')
        else:
            return Wish.objects.filter(
                user_id=user_id,
                visibility__in=['public', 'link'])
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]