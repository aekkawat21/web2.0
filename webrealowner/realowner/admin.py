from django.contrib import admin
from .models import *

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'age', 'gender', 'phone_number', 'transferred_items_count')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('gender', 'age')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'email', 'age', 'gender', 'phone_number')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('picture', 'transferred_items_count'),
        }),
    )

admin.site.register(UserProfile, UserProfileAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'brand', 
        'model', 
        'color', 
        'serial_number', 
        'category', 
        'store_date_of_purchase', 
        'store_of_purchase', 
        'warranty', 
        'previous_owner',
        'description',
    )

    list_filter = ('category', 'brand', 'store_of_purchase')

    search_fields = ('brand', 'model', 'serial_number', 'previous_owner')

    date_hierarchy = 'store_date_of_purchase'
    
    ordering = ('-store_date_of_purchase',)

admin.site.register(Item, ItemAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', ) 
    search_fields = ('name',)  

admin.site.register(Category, CategoryAdmin)    