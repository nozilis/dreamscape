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
  PRIVATE = 'private'
  LINK = 'link'
  PUBLIC = 'public'
    
  VISIBILITY_CHOICES = [
      (PRIVATE, 'Private'),
      (LINK, 'Link only'),
      (PUBLIC, 'Public'),
  ]
    
  visibility = models.CharField(
      max_length=10,
      choices=VISIBILITY_CHOICES,
      default=PRIVATE
  )

  DREAMING = 'dreaming'
  IN_PROCESS = 'in_process'
  DONE = 'done'
    
  STATUS_CHOICES = [
      (DREAMING, 'Мечтаю'),
      (IN_PROCESS, 'В процессе'),
      (DONE, 'Выполнено'),
  ]
    
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default='Мечтаю'
  )
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  last_wish_at = models.DateTimeField(auto_now=True)
  images = models.ImageField(upload_to='images/wish_images', blank=True, null=True)
  location = models.CharField(max_length=200, blank=True)
  latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  gift_url = models.URLField(max_length=1000, blank=True)
  is_done = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.title