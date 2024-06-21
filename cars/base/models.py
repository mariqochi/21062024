

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

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
    
    
    
    
    
    
    
class CarAvailability(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Availability for {self.car} on {self.date}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    loc_from = models.CharField(max_length=50, default="")
    loc_to = models.CharField(max_length=50, default="")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.car}"

    def save(self, *args, **kwargs):
        # Calculate total cost based on the number of days and car's price
        if self.start_date and self.end_date and self.car.price:
            self.total_cost = (self.end_date - self.start_date).days * self.car.price
        super().save(*args, **kwargs)

    def clean(self):
        # Check if the car is available for the selected dates
        if self.start_date and self.end_date:
            car_availabilities = CarAvailability.objects.filter(
                car=self.car,
                date__range=[self.start_date, self.end_date]
            )
            if car_availabilities.count() != (self.end_date - self.start_date).days + 1:
                raise ValidationError('Car is not available for the selected dates.')
            # Check if the car is already booked by another user for the same period
            conflicting_bookings = Booking.objects.filter(
                car=self.car,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            ).exclude(user=self.user)
            if conflicting_bookings.exists():
                raise ValidationError('Car is not available for the selected dates.')
    # def __str__(self):
    #     return f"Booking {self.id} - {self.user.username} - {self.car}"

    # def save(self, *args, **kwargs):
    #     # Calculate total cost based on the number of days and car's price
    #     if self.start_date and self.end_date and self.car.price:
    #         self.total_cost = (self.end_date - self.start_date).days * self.car.price
    #     super().save(*args, **kwargs)

    # def clean(self):
    #     # Check if the car is available for the selected dates
    #     if self.start_date and self.end_date:
    #         car_availabilities = CarAvailability.objects.filter(
    #             car=self.car,
    #             date__range=[self.start_date, self.end_date]
    #         )
    #         if car_availabilities.count() != (self.end_date - self.start_date).days + 1:
    #             raise ValidationError('Car is not available for the selected dates.')
