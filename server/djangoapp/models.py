# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('ESTATE', 'Estate'),
    ]

    type = models.CharField(max_length=10, choices=CAR_TYPES, default='Hatchback')
    year = models.IntegerField(default=2023, 
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ])

    def __str__(self):
        return self.name

