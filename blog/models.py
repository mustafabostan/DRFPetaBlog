from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission

class CustomUser(AbstractUser):
    phone_code = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def assign_permission(self, permission):
        permission = Permission.objects.get(codename=permission)
        self.user_permissions.add(permission)

    def remove_permission(self, permission):
        permission = Permission.objects.get(codename=permission)
        self.user_permissions.remove(permission)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name
    
    

class Blog(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.title