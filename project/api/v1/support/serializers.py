from rest_framework import serializers

from apps.support.models import (
    Article, ArticleCategory, ArticlePhoto, Catalog, CatalogCategory,
    Certificate,
)
from api.v1.file.serializers import FileSerializer
from apps.helpers.serializers import FixAbsolutePathCkEditorSerializer


class ArticlePhotoSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = ArticlePhoto
        fields = ('id', 'created_at', 'photo',)
        read_only_fields = ('id', 'created_at',)


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ('id', 'created_at', 'name', 'slug',)
        read_only_fields = ('id', 'created_at',)


class ArticleSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    article_photos = ArticlePhotoSerializer(many=True)
    category = ArticleCategorySerializer()
    text = FixAbsolutePathCkEditorSerializer()

    class Meta:
        model = Article
        fields = (
            'id', 'created_at', 'category', 'name', 'slug', 'description',
            'photo', 'text', 'article_photos',
        )
        read_only_fields = ('id', 'created_at',)


class CatalogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCategory
        fields = ('id', 'created_at', 'name', 'slug', 'order',)
        read_only_fields = ('id', 'created_at',)


class SupportCatalogSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    file = FileSerializer()
    category = CatalogCategorySerializer()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'created_at',
            'category',
            'name',
            'slug',
            'description',
            'photo',
            'file',
            'ordering_num',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class ShortSupportCatalogSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = ('id', 'file',)

    def get_file(self, obj):
        filepath = FileSerializer(obj.file, context=self.context).data['file']
        request = self.context['request']
        absurl = request.build_absolute_uri(filepath)
        return absurl


class CertificateSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    file = FileSerializer()

    class Meta:
        model = Certificate
        fields = ('id', 'created_at', 'name', 'description', 'photo', 'file',)
        read_only_fields = ('id', 'created_at',)
