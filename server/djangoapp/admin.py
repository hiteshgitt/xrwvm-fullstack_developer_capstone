from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class for displaying CarModel instances within CarMake admin
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3  # Number of extra forms to display


# CarMakeAdmin class to customize the CarMake admin page
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # Include CarModelInline to show related CarModels
    list_display = ('name', 'description')  # Fields to display in the list view
    search_fields = ['name']  # Enable search by name
    # You can add more customizations here, e.g., list_filter, ordering


# CarModelAdmin class to customize the CarModel admin page
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  # Fields to display
    list_filter = ('car_make', 'type', 'year')  # Enable filtering
    search_fields = ['name', 'car_make__name']  # Search by model name and car make name


# Register the models with the custom admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
