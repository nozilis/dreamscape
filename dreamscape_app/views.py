from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Wish, User
from .serializers import CategorySerializer, WishSerializer, RegisterSerializer, UserProfileSerializer
from .permissions import UserAccessPermission
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

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
        return Wish.objects.filter(
            user_id=user_id,
            visibility__in=['public', 'link'])
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        return response
    
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user