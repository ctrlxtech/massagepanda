from django.contrib import admin
from .models import Staff, Area, Therapist, SMSTemplate, Interval, Schedule
from django.contrib.auth.models import User

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class IntervalInline(NestedStackedInline):
    model = Interval
    fk_name = "therapist"
    extra = 1

class ScheduleInline(NestedStackedInline):
    model = Schedule
    fk_name = "therapist"
    extra = 1
    inlines = [IntervalInline, ]

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

class TherapistAdmin(NestedModelAdmin):
    list_display = ('phone', 'get_name', 'gender')
    list_filter = ['gender']
    inlines = (TherapistAreaInline, ScheduleInline)

    def get_name(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)
    get_name.short_description = 'name'
    get_name.admin_order_field = 'therapist__name'

admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(SMSTemplate, TemplateAdmin)
