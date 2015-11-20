from django.contrib import admin, messages
from .models import Order, OrderTherapist, Coupon, ServiceCoupon
from feedback.models import Feedback
from services.models import Service
from services.views import redeemRefer
from manager.views import sendFeedbackEmail

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.db import transaction

import stripe

def sendOrderEmail(order, template, subject, extra=[]):
    stripe.api_key = settings.STRIPE_KEY
    stripeCharge = stripe.Charge.retrieve(order.stripe_token)
    from_email, to = settings.SERVER_EMAIL, order.email
    text_content = 'This is an email containing your order.'
    context = {'order': order, 'stripeCharge': stripeCharge}
    real_context = dict(context)
    real_context.update(extra)
    html_content = get_template(template).render(Context(real_context))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class OrderTherapistInline(admin.StackedInline):
    model = OrderTherapist
    extra = 1

class FeedbackInline(admin.StackedInline):
    model = Feedback
    readonly_fields = ('code', 'rated', 'rating', 'comment', 'request_count')

class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('service', )
    list_display = ('order_id', 'get_service', 'recipient', 'service_datetime', 'created_at', 'status', 'get_feedback')
    list_display_links = ('order_id', 'get_service', 'recipient', 'service_datetime', 'created_at')
    search_fields = ['id', ]
    readonly_fields = ('order_id', 'need_table', 'parking_info', 'stripe_token', 'created_at' )
    ordering = ['-created_at',]

    inlines = [
        OrderTherapistInline, FeedbackInline
    ]

    actions = ['mark_charged', 'punish', 'mark_canceled', 'send_feedback_email']

    def order_id(self, obj):
        return '%s' % (obj.id.int >> 96)

    def get_service(self, obj):
        return '%s For %.1f' % (obj.service.service_type, obj.service.service_time)
    get_service.short_description = 'service'
    get_service.admin_order_field = 'service'

    def get_feedback(self, obj):
        return '%s' % (obj.feedback.rating)
    get_feedback.short_description = 'feedback'
    get_feedback.admin_order_field = 'feedback'

    def mark_refunded(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0;
      for order in queryset:
        try:
            stripe.Refund.create(charge=order.stripe_token)
            order.status = '5'
            order.save()

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "%s can't be marked as refunded. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as refunded." % count)

    @transaction.atomic
    def mark_charged(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.status == '3' or order.status != '1':
                raise ValueError("Order is not chargeable[" + order.status + "]")

            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.retrieve(order.stripe_token)
            ch.capture()

            sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda')

            order.status = '4'
            order.stripe_token = ch.id
            order.save()

            redeemRefer(order)

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be marked as charged. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as charged." % count)
      
    def punish(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.retrieve(order.stripe_token)
            ch.capture(
                amount=order.amount
            )

            sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda', {"customerCanceled": True})

            order.status = '6'
            order.stripe_token = ch.id
            order.save()

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be punished. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully punished." % count)
   
    def charge_40(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.status == '3':
                raise ValueError("Order has been canceled")
            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.retrieve(order.stripe_token)
            ch.capture(
                amount=4000 # amount in cents, again
            )

            order.status = '7'
            order.stripe_token = ch.id
            order.save()

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be marked as charged. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as charged." % count)

    def charge_10(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.status == '3':
                raise ValueError("Order has been canceled")
            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.retrieve(order.stripe_token)
            ch.capture(
                amount=1000 # amount in cents, again
            )

            order.status = '6'
            order.stripe_token = ch.id
            order.save()

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be marked as charged. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as charged." % count)
 
    def mark_canceled(self, request, queryset):
      count = 0
      for order in queryset:
        try:
            stripe.Refund.create(charge=order.stripe_token)
            order.status = '3'
            order.save()

            sendOrderEmail(order, 'payment/order_canceled_email.html', 'Your order has been canceled! - MassagePanda')

            count += 1
        except:
            self.message_user(request, "Order(number: %s) can't be marked as canceled." % order.id, level=messages.ERROR)

      self.message_user(request, "%s successfully marked as canceled." % count)
    
    def send_feedback_email(self, request, queryset):
      count = 0
      for order in queryset:
        try:
          sendFeedbackEmail(request, order.id)
          count += 1
        except:
          self.message_user(request, "Email can't be sent for order[%s]." % order.id, level=messages.ERROR)
          pass
      self.message_user(request, "%s email(s) sent." % count)

class ServiceCouponInline(admin.StackedInline):
    model = ServiceCoupon
    extra = 1

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'quantity', 'used', 'start_date', 'end_date']
    readonly_fields = ('used',)

    inlines = [
        ServiceCouponInline,
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
