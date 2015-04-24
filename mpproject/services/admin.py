from django.contrib import admin

from .models import Service, ServiceImage 
# Register your models here.

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 3

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'service_time', 'service_fee')
    list_filter = ['service_time', 'service_fee']
    search_fields = ['service_type']
    inlines = [ServiceImageInline]

admin.site.register(Service, ServiceAdmin)
