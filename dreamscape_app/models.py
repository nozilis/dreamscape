from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  bio = models.TextField(blank=True)
  age = models.IntegerField(blank=True, null=True)
  avatar = models.ImageField(upload_to='images/user_avatar_images/', blank=True, null=True)
  background_image = models.ImageField(upload_to='images/user_background_images/', blank=True, null=True)

  def __str__(self):
    return self.username

class Category(models.Model):
  title = models.CharField(max_length=64)

class Wish(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  last_wish_at = models.DateTimeField(auto_now=True)
  images = models.ImageField(upload_to='images/wish_images')
  location = models.CharField(max_length=200, blank=True)
  gift_url = models.URLField(max_length=1000, blank=True)
  is_done = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.title