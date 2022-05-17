import os
import base64

from rest_framework import serializers

from constance import config
from pysendpulse.pysendpulse import PySendPulse

from apps.order.models import Order
from apps.cart.models import Cart
from .helpers import get_order_info_for_email, make_excel_about_order

SENDPULSE_ID = os.environ.get('SENDPULSE_ID', None)
SENDPULSE_SECRET = os.environ.get('SENDPULSE_SECRET', None)
SENDPULSE_EMAIL_FROM = os.environ.get('SENDPULSE_EMAIL_FROM', None)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'delivery_type', 'fio', 'email', 'phone', 'inn', 'name_company', 'comment')
        read_only_fields = ('id', 'created_at')


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('delivery_type', 'fio', 'email', 'phone', 'inn', 'name_company', 'comment', 'requisites')

    def create(self, validated_data: dict) -> Order:
        order = super().create(validated_data)

        cart = Cart.objects.get(pk=self.context['cart_id'])
        cart.order = order
        cart.save()

        text, html = get_order_info_for_email(order, cart)
        excel_filedest = make_excel_about_order(order, cart, self.context["request"])
        self.send_email_about_order(order, excel_filedest, text, html)
        return order

    def send_email_about_order(self, order: Order, excel_dest: str, text: str, html: str):
        excel_file = open(excel_dest, 'rb')
        attachments_bin = {excel_dest.split("/")[-1]: base64.b64encode(excel_file.read()).decode("utf-8")}
        excel_file.close()

        for requisite in [requisite for requisite in order.requisites.all()]:
            key = requisite.file.path.split('/')[-1]
            requisite_file = open(requisite.file.path, 'rb')
            value = base64.b64encode(requisite_file.read()).decode("utf-8")
            attachments_bin[key] = value
            requisite_file.close()

        SPApiProxy = PySendPulse(SENDPULSE_ID, SENDPULSE_SECRET, 'memcached')
        SPApiProxy.smtp_send_mail({
            'subject': 'Новый заказ',
            'text': text,
            'html': html,
            'from': {'name': 'service', 'email': SENDPULSE_EMAIL_FROM},
            'to': [{'name': 'info', 'email': config.email_about_order}],
            'attachments_binary': attachments_bin,
        })
