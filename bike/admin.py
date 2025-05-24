from django.contrib import admin
from .models import Component, Bike


# Register your models here.
class ComponentInline(admin.StackedInline):
    model = Component
    can_delete = False
    verbose_name_plural = "component"


class BikeAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


# admin.site.unregister(Bike)
admin.site.register(Bike, BikeAdmin)
