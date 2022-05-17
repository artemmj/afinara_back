from rest_framework import serializers


class SearchQueryParamsSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
