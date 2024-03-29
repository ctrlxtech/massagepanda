from django.contrib import admin

from .models import Service, Group, ServiceGroup, ServiceImage 
# Register your models here.

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 3

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'service_time', 'service_fee')
    list_filter = ['service_time', 'service_fee']
    search_fields = ['service_type']
    inlines = [
        ServiceImageInline
    ]

class ServiceGroupInline(admin.TabularInline):
    model = ServiceGroup
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', )
    search_fields = ['group_name', ]
    inlines = [
        ServiceGroupInline
    ]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Group, GroupAdmin)
