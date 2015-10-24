from django.contrib import admin, messages
from .models import Order, OrderTherapist, Coupon
from feedback.models import Feedback
from services.models import Service
from services.views import redeemRefer
from manager.views import sendFeedbackEmail

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

import stripe

def sendOrderEmail(order, template, subject):
    stripe.api_key = settings.STRIPE_KEY
    stripeToken = stripe.Token.retrieve(order.stripe_token)
    from_email, to = settings.SERVER_EMAIL, order.email
    text_content = 'This is an email containing your order.'
    html_content = get_template(template).render(Context({'order': order, 'stripeToken': stripeToken}))
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
    list_display = ('id', 'get_service', 'recipient', 'service_datetime', 'status', 'get_feedback')
    list_display_links = ('id', 'get_service', 'recipient', 'service_datetime')
    search_fields = ['id', ]
    readonly_fields = ('id', 'need_table', 'parking_info', 'stripe_token', 'status')

    inlines = [
        OrderTherapistInline, FeedbackInline
    ]

    actions = ['mark_refunded', 'mark_charged', 'charge_40', 'charge_10', 'mark_canceled', 'send_feedback_email']

    def get_service(self, obj):
        return '%s For %.1f' % (obj.service.service_type, obj.service.service_time)
    get_service.short_description = 'service'
    get_service.admin_order_field = 'order__service'

    def get_feedback(self, obj):
        return '%s' % (obj.feedback.rating)
    get_service.short_description = 'feedback'
    get_service.admin_order_field = 'order__feedback'

    def mark_refunded(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0;
      for order in queryset:
        try:
            stripe.Refund.create(charge=order.stripe_token)
            order.status = 5
            order.save()

            count += 1
        except stripe.error.StripeError, e:
            self.message_user(request, "%s can't be marked as refunded. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as refunded." % count)

    def mark_charged(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.status == 3 or order.status != 1:
                raise ValueError("Order is not chargeable")

            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.create(
                amount=order.amount, # amount in cents, again
                currency="usd",
                customer=stripeCustomerId,
                source=order.stripe_token,
                description="Admin charge"
            )

            sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda')

            order.status = 4
            order.stripe_token = ch.id
            order.save()

            redeemRefer(order)

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be marked as charged. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully marked as charged." % count)
    
    def charge_40(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
        try:
            if order.status == 3:
                raise ValueError("Order has been canceled")
            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.create(
                amount=4000, # amount in cents, again
                currency="usd",
                customer=stripeCustomerId,
                source=order.stripe_token,
                description="Admin charge"
            )

            order.status = 7
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
            if order.status == 3:
                raise ValueError("Order has been canceled")
            if order.customer is not None:
                stripeCustomerId = order.customer.stripe_customer_id
            else:
                stripeCustomerId = None

            ch = stripe.Charge.create(
                amount=1000, # amount in cents, again
                currency="usd",
                customer=stripeCustomerId,
                source=order.stripe_token,
                description="Admin charge"
            )

            order.status = 6
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
            order.status = 3
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
          sendFeedbackEmail(order.id)
          count += 1
        except:
          self.message_user(request, "Email can't be sent for order[%s]." % order.id, level=messages.ERROR)
          pass
      self.message_user(request, "%s email(s) sent." % count)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount']

admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
