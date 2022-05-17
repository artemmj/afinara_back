from rest_framework import serializers

from apps.pages.models import SolutionForArea, CompleteProject, AboutProduction
from api.v1.file.serializers import FileSerializer
from apps.helpers.serializers import FixAbsolutePathCkEditorSerializer
from api.v1.catalog.serializers import ProductSerializer


class CompleteProjectSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    text = FixAbsolutePathCkEditorSerializer()

    class Meta:
        model = CompleteProject
        fields = ('id', 'created_at', 'title', 'photo', 'text',)
        read_only_fields = ('id', 'created_at',)


class ShortSolutionForAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionForArea
        fields = ('id', 'name', 'slug')


class SolutionForAreaSerializer(serializers.ModelSerializer):
    photo = FileSerializer()
    complete_projects = CompleteProjectSerializer(many=True, read_only=True)
    article = FixAbsolutePathCkEditorSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = SolutionForArea
        fields = (
            'id', 'created_at', 'name', 'slug', 'photo', 'article',
            'complete_projects', 'products',
        )
        read_only_fields = ('id', 'created_at',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class AboutProductionSerializer(serializers.ModelSerializer):
    preview_for_mainpage = FileSerializer()
    photo = FileSerializer()
    article = FixAbsolutePathCkEditorSerializer()

    class Meta:
        model = AboutProduction
        fields = (
            'id', 'created_at', 'name', 'slug', 'preview_for_mainpage',
            'photo', 'article',
        )
        read_only_fields = ('id', 'created_at',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
