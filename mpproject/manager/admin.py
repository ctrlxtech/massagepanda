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
    fk_name = "staff"
    extra = 0

class TherapistAreaInline(admin.TabularInline):
    model = Area
    fk_name = "therapist"
    extra = 0

class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ['gender', ]
    search_fields = ['first_name', 'last_name']
    inlines = [AreaInline,]

class TemplateAdmin(admin.ModelAdmin):
    pass

class TherapistAdmin(admin.ModelAdmin):
    list_display = ('phone', 'get_name', 'gender')
    list_filter = ['gender']
    inlines = (TherapistAreaInline, )

    def get_name(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)
    get_name.short_description = 'name'
    get_name.admin_order_field = 'therapist__name'

admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(SMSTemplate, TemplateAdmin)
