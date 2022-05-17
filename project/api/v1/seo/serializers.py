from rest_framework import serializers

from apps.seo.models import Seo


class SeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seo
        fields = (
            'id', 'name', 'route', 'title', 'h1', 'description', 'keywords',
            'canonical_rel', 'domain',
        )
