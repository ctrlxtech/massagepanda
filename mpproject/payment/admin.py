from django.contrib import admin, messages
from .models import Order, OrderTherapist, Coupon
from feedback.models import Feedback
from services.models import Service

from django.conf import settings

import stripe

# Register your models here.
class OrderTherapistInline(admin.StackedInline):
    model = OrderTherapist
    extra = 1

class FeedbackInline(admin.StackedInline):
    model = Feedback
    readonly_fields = ('code', 'rated', 'rating', 'comment', 'request_count')

class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('service', )
    list_display = ('order_number', 'get_service', 'recipient', 'service_datetime', 'status', 'get_feedback')
    list_display_links = ('order_number', 'get_service', 'recipient', 'service_datetime')
    search_fields = ['order_number', ]
    readonly_fields = ('order_number', 'stripe_token', 'status')

    inlines = [
        OrderTherapistInline, FeedbackInline
    ]

    actions = ['make_refunded', 'make_charged']

    def get_service(self, obj):
        return '%s For %.1f' % (obj.service.service_type, obj.service.service_time)
    get_service.short_description = 'service'
    get_service.admin_order_field = 'order__service'

    def get_feedback(self, obj):
        return '%s' % (obj.feedback.rating)
    get_service.short_description = 'feedback'
    get_service.admin_order_field = 'order__feedback'

    def make_refunded(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0;
      for order in queryset:
        try:
            stripe.Refund.create(charge=order.stripe_token)
            order.status = 5
            order.save()

            count += 1
        except stripe.error.StripeError, e:
            self.message_user(request, "%s can't be marked as refunded. Error: %s" % (order.order_number, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as refunded." % count)

    def make_charged(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0;
      for order in queryset:
        try:
            ch = stripe.Charge.create(
                amount=order.amount, # amount in cents, again
                currency="usd",
                source=order.stripe_token,
                description="Admin charge"
            )

            order.status = 4
            order.stripe_token = ch.id
            order.save()

            count += 1
        except stripe.error.StripeError, e:
            self.message_user(request, "Order(number: %s) can't be marked as charged. Error: %s" % (order.order_number, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as charged." % count)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount']

admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
