from rest_framework import serializers

from apps.catalog.models import Catalog
from api.v1.file.serializers import FileSerializer
from apps.helpers.serializers import EagerLoadingSerializerMixin


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'slug', 'description', 'ordering_num', 'parent')
        depth = 2


class CatalogNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'slug', 'ordering_num', 'parent')

    def get_name(self, obj):
        return obj.__str__()


class CatalogMainSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    photo = FileSerializer(allow_null=True)

    select_related_fields = ['photo']

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'slug', 'photo', 'ordering_num', 'parent')
        depth = 2
