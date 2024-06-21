

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=255, null=True)  # Use EmailField for email
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # Define related_names to avoid clashes
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='users',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='user_groups',  # Adjust related_name here
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    def __str__(self):
        return self.username


class Type(models.Model):
    name=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    


class Car(models.Model):
    make = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=20, null=True, blank=True)
    manufacturing_year = models.IntegerField()
    fuel_consumption = models.DecimalField(max_digits=4, decimal_places=2)
    color = models.CharField(max_length=20, null=True, blank=True)
    num_seats = models.IntegerField()
    car_type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model}"