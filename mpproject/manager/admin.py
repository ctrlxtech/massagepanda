from django.contrib import admin
from .models import Staff, Area, Therapist, SMSTemplate
from django.contrib.auth.models import User


class TherapistInline(admin.StackedInline):
    model = Therapist
    can_delete = False
    verbose_name_plural = 'therapist'

class UserInline(admin.StackedInline):
    model = User

class AreaInline(admin.TabularInline):
    model = Area
    extra = 0

class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ['gender', ]
    search_fields = ['first_name', 'last_name']
    inlines = [AreaInline,]

class TemplateAdmin(admin.ModelAdmin):
    pass

class TherapistAdmin(admin.ModelAdmin):
    list_display = ('phone', 'gender')
    list_filter = ['gender']
    #inlines = (UserInline, )

admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(SMSTemplate, TemplateAdmin)
