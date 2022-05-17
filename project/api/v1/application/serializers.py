from rest_framework import serializers
from apps.application.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(allow_blank=False)
    email = serializers.CharField(allow_blank=False)

    class Meta:
        model = Application
        fields = (
            'id',
            'name',
            'phone',
            'email',
            'files',
            'comment',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')
