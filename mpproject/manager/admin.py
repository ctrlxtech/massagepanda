from django.contrib import admin

from .models import Staff
# Register your models here.
class StaffAdmin(admin.ModelAdmin):
    list_filter = ['gender', 'name']
    search_fields = ['name']

admin.site.register(Staff, StaffAdmin)
