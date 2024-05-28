from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(UserProfile)

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