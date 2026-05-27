from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Category, Wish, User
from .serializers import CategorySerializer, WishSerializer, RegisterSerializer, UserProfileSerializer
from .permissions import UserAccessPermission
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from .tasks import greetings_email
from django.core.cache import cache

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class WishViewSet(ModelViewSet):
    serializer_class = WishSerializer
    permission_classes = [IsAuthenticated, UserAccessPermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')  
        if user_id is None:
            return Wish.objects.filter(user=self.request.user).order_by('-created_at')
        user_id = int(user_id)  
        if user_id == self.request.user.id:
            return Wish.objects.filter(user=self.request.user).order_by('-created_at')
        cache_response = cache.get(f'wishlist_{user_id}')
        if cache_response is not None:
            return cache_response
        else:
            new_cache_data = Wish.objects.filter(user_id=user_id, visibility__in=['public', 'link'])
            cache.set(f'wishlist_{user_id}', new_cache_data, timeout=3600)
        return new_cache_data

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f'wishlist_{self.request.user.id}')

    def partial_update(self, request, *args, **kwargs): 
        response = super().partial_update(request, *args, **kwargs)
        cache.delete(f'wishlist_{self.request.user.id}')
        return response

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete(f'wishlist_{self.request.user.id}')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='ID of the user whose wishes to retrieve'
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        greetings_email.delay(user.email)
        return response
    
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user