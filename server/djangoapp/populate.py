from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import IntegrityError
from ...models import CarMake, CarModel


class Command(BaseCommand):
    help = 'Populates the CarMake and CarModel models with sample data'

    def handle(self, *args, **options):
        car_makes = [
            {'name': 'Toyota', 'description': 'Reliable and fuel-efficient vehicles'},
            {'name': 'Ford', 'description': 'Innovative American cars'},
            {'name': 'BMW', 'description': 'Luxury vehicles from Germany'},
            {'name': 'Honda', 'description': 'Affordable and durable cars'},
            {'name': 'Mercedes', 'description': 'Premium German automobiles'},
            {'name': 'Chevrolet', 'description': 'Wide range of American cars'},
        ]

        car_models = [
            {'name': 'Corolla', 'car_make': 'Toyota', 'type': 'SEDAN', 'year': 2023},
            {'name': 'Camry', 'car_make': 'Toyota', 'type': 'SEDAN', 'year': 2022},
            {'name': 'F-150', 'car_make': 'Ford', 'type': 'SUV', 'year': 2023},
            {'name': 'Mustang', 'car_make': 'Ford', 'type': 'COUPE', 'year': 2021},
            {'name': 'X5', 'car_make': 'BMW', 'type': 'SUV', 'year': 2022},
            {'name': '3 Series', 'car_make': 'BMW', 'type': 'SEDAN', 'year': 2023},
            {'name': 'Civic', 'car_make': 'Honda', 'type': 'SEDAN', 'year': 2023},
            {'name': 'Accord', 'car_make': 'Honda', 'type': 'SEDAN', 'year': 2021},
            {'name': 'C-Class', 'car_make': 'Mercedes', 'type': 'SEDAN', 'year': 2022},
            {'name': 'S-Class', 'car_make': 'Mercedes', 'type': 'SEDAN', 'year': 2023},
            {'name': 'Equinox', 'car_make': 'Chevrolet', 'type': 'SUV', 'year': 2022},
            {'name': 'Malibu', 'car_make': 'Chevrolet', 'type': 'SEDAN', 'year': 2021},
        ]

        for car_make in car_makes:
            try:
                make, created = CarMake.objects.get_or_create(
                    name=car_make['name'], defaults={'description': car_make['description']}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created car make: {make.name}"))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f"Car make {car_make['name']} already exists"))

        for car_model in car_models:
            try:
                make = CarMake.objects.get(name=car_model['car_make'])
                model, created = CarModel.objects.get_or_create(
                    name=car_model['name'],
                    car_make=make,
                    defaults={'type': car_model['type'], 'year': car_model['year']}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created car model: {model.name}"))
            except CarMake.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Car make {car_model['car_make']} not found"))
