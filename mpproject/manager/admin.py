from django.contrib import admin

from .models import Staff
# Register your models here.
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ['gender', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

admin.site.register(Staff, StaffAdmin)
