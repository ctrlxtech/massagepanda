from django.contrib import admin, messages
from .models import Order, OrderTherapist, Coupon, ServiceCoupon
from feedback.models import Feedback
from services.models import Service
from services.views import redeemRefer
from manager.views import sendFeedbackEmail
from referral.models import ReferralCredit

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

def chargeOrder(order):
    if order.credit_used == order.amount:
      return None
    if order.credit_used > order.amount:
      credit_refunded = order.credit_used - order.amount
      aCredit = order.customer.referralcredit_set.all().latest('id').accumulative_credit + credit_refunded
      rCredit = ReferralCredit(customer=order.customer, adjustment=True, credit=credit_refunded, accumulative_credit=aCredit)
      rCredit.save()
      ch = stripe.Refund.create(charge=order.stripe_token)
    else:
      ch = stripe.Charge.retrieve(order.stripe_token)
      if ch.amount == 100: # Refund place holder amount
          stripe.Refund.create(charge=order.stripe_token)
          order.amount = 0
      else:
          amount_to_charge = int(order.amount - order.credit_used)
          ch.capture(amount=amount_to_charge)
    
    return ch.id

class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('service', )
    list_display = ('external_id', 'get_service', 'recipient', 'service_datetime', 'created_at', 'status', 'get_feedback')
    list_display_links = ('external_id', 'get_service', 'recipient', 'service_datetime', 'created_at')
    search_fields = ['external_id', ]
    readonly_fields = ('external_id', 'need_table', 'parking_info', 'credit_used', 'stripe_token', 'created_at' )
    ordering = ['-created_at',]

    inlines = [
        OrderTherapistInline, FeedbackInline
    ]

    actions = ['mark_charged', 'mark_refunded', 'punish', 'mark_canceled', 'send_shipped_email', 'send_feedback_email']

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
            if order.status == '5':
                raise ValueError("Order[%s] has already been refunded" % (order.id.int >> 96))

            ch = stripe.Charge.retrieve(order.stripe_token)
            refund_amount = max(ch.amount - order.amount, 0)
            stripe.Refund.create(
                charge=order.stripe_token,
                amount=refund_amount)

            sendOrderEmail(order, 'payment/partial_refund_email.html', 'Your refund is on the way! - MassagePanda', {"refund_amount": refund_amount})

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

            stripeId = chargeOrder(order)

            order.status = '4'
            order.stripe_token = stripeId
            order.save()

            # sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda')
            # sendFeedbackEmail(request, order.id)

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

            stripeId = chargeOrder(order)

            order.status = '6'
            order.stripe_token = stripeId
            order.save()

            sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda', {"customerCanceled": True})

            count += 1
        except (stripe.error.StripeError, ValueError) as e:
            self.message_user(request, "Order(number: %s) can't be punished. Error: %s" % (order.id, e), level=messages.ERROR)

      self.message_user(request, "%s successfully punished." % count)
   
    @transaction.atomic
    def mark_canceled(self, request, queryset):
      stripe.api_key = settings.STRIPE_KEY
      count = 0
      for order in queryset:
            if order.credit_used != 0:
              aCredit = order.customer.referralcredit_set.all().latest('id').accumulative_credit + order.credit_used
              rCredit = ReferralCredit(customer=order.customer, adjustment=True, credit=order.credit_used, accumulative_credit=aCredit)
              rCredit.save()

            if order.coupon and order.coupon.quantity >= 0:
              coupon = order.coupon
              coupon.quantity += 1
              coupon.used -= 1
              coupon.save()

            stripe.Refund.create(charge=order.stripe_token)
            order.status = '3'
            order.save()

            sendOrderEmail(order, 'payment/order_canceled_email.html', 'Your order has been canceled! - MassagePanda')

            count += 1

      self.message_user(request, "%s successfully marked as canceled." % count)

    def send_shipped_email(self, request, queryset):
      count = 0
      for order in queryset:
        try:
          sendOrderEmail(order, 'payment/order_shipped_email.html', 'Your order has been shipped! - MassagePanda')
          count += 1
        except:
          self.message_user(request, "Email can't be sent for order[%s]." % order.id, level=messages.ERROR)
          pass
      self.message_user(request, "%s email(s) sent." % count)
  
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
    list_filter = ['is_groupon', 'is_gilt']
    readonly_fields = ('used',)

    inlines = [
        ServiceCouponInline,
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
