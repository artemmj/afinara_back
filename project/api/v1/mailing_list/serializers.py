import os
import logging

from rest_framework import serializers

from pysendpulse.pysendpulse import PySendPulse

from apps.mailing_list.models import MailRecipient

logger = logging.getLogger()

SENDPULSE_ID = os.environ.get('SENDPULSE_ID', None)
SENDPULSE_SECRET = os.environ.get('SENDPULSE_SECRET', None)
SENDPULSE_EMAIL_FROM = os.environ.get('SENDPULSE_EMAIL_FROM', None)


class MailRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailRecipient
        fields = ('id', 'created_at', 'email', 'enabled',)
        read_only_fields = ('id', 'created_at',)

    def create(self, validated_data):
        SPApiProxy = PySendPulse(SENDPULSE_ID, SENDPULSE_SECRET, 'memcached')
        SPApiProxy.smtp_send_mail({
            'subject': 'ТЕСТ. Вы подписались на email-рассылку',
            'html': 'ТЕСТ. Текст текст текст<br>',
            'text': 'ТЕСТ. Текст текст текст',
            'from': {
                'name': 'service',
                'email': SENDPULSE_EMAIL_FROM
            },
            'to': [
                {
                    'name': validated_data['email'].split('@')[0],
                    'email': validated_data['email']
                },
            ],
        })
        obj = MailRecipient.objects.create(**validated_data)
        return obj
