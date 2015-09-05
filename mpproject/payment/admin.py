from django.contrib import admin
from .models import Order, OrderTherapist
from feedback.models import Feedback
from services.models import Service

# Register your models here.
class OrderTherapistInline(admin.StackedInline):
    model = OrderTherapist
    extra = 1

class FeedbackInline(admin.StackedInline):
    model = Feedback
    readonly_fields = ('rating', 'comment', )

class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('service', )
    list_display = ('id', 'get_service', 'recipient', 'service_datetime', 'get_feedback')
    list_display_links = ('id', 'get_service', 'recipient', 'service_datetime')
    readonly_fields = ('order_number', 'stripe_token')

    inlines = [
        OrderTherapistInline, FeedbackInline
    ]

    def get_service(self, obj):
        return '%s For %.1f' % (obj.service.service_type, obj.service.service_time)
    get_service.short_description = 'service'
    get_service.admin_order_field = 'order__service'

    def get_feedback(self, obj):
        return '%s' % (obj.feedback.rating)
    get_service.short_description = 'feedback'
    get_service.admin_order_field = 'order__feedback'

admin.site.register(Order, OrderAdmin)
