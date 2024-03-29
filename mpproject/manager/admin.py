from django.contrib import admin
from .models import Staff, Area, Therapist, SMSTemplate, Interval, Schedule
from django.contrib.auth.models import User

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class IntervalInline(NestedStackedInline):
    model = Interval
    fk_name = "schedule"
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
    list_display = ('phone', 'get_name', 'gender', 'get_rating')
    list_filter = ['gender']
    inlines = (TherapistAreaInline, ScheduleInline)
    readonly_fields = ('user', 'rating', 'rate_count')

    def get_rating(self, obj):
        return '%s' % (0 if obj.rate_count == 0 else (obj.rating / obj.rate_count))
    get_rating.short_description = 'rating'

    def get_name(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)
    get_name.short_description = 'name'
    get_name.admin_order_field = 'therapist__name'

admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(SMSTemplate, TemplateAdmin)
