from django.contrib import admin
from .models import (
    CarMake,
    CarModel
)


class CarModelInline(admin.TabularInline):  # Inline for CarModel in CarMakeAdmin
    model = CarModel
    extra = 1


class CarModelAdmin(admin.ModelAdmin):  # Admin for CarModel
    list_display = ('name', 'car_make', 'type', 'year')
    list_filter = ('type', 'year', 'car_make')
    search_fields = ('name',)


class CarMakeAdmin(admin.ModelAdmin):  # Admin for CarMake with CarModelInline
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    search_fields = ('name',)


# Register models with admin site
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
