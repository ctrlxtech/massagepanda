from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from customers.models import Customer

# Define a new User admin
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'stripe_customer_id')

admin.site.register(Customer, CustomerAdmin)
