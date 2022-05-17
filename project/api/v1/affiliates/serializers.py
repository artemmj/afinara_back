import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers
from constance import config
from drf_yasg.utils import swagger_serializer_method

from apps.affiliates.models import (
    Affiliate, Director, SocialNetwork, Employee, Partner, TermsOfUseFiles,Requisite
)
from api.v1.file.serializers import FileSerializer
from apps.helpers.serializers import FixAbsolutePathCkEditorSerializer

User = get_user_model()

logger = logging.getLogger()


class DirectorSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = Director
        fields = (
            'id', 'created_at', 'fio', 'position', 'description', 'photo',
        )
        read_only_fields = ('id', 'created_at',)


class SocialNetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('id', 'created_at', 'type', 'link')


class EmployeeSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = Employee
        fields = (
            'id', 'created_at', 'fio', 'position', 'photo', 'phone', 'email',
        )
        read_only_fields = ('id', 'created_at',)


class PartnerSerializer(serializers.ModelSerializer):
    logo = FileSerializer()
    text = FixAbsolutePathCkEditorSerializer()

    class Meta:
        model = Partner
        fields = ('id', 'created_at', 'logo', 'text',)
        read_only_fields = ('id', 'created_at',)


class TermsOfUseSerializer(serializers.ModelSerializer):
    map_site = serializers.SerializerMethodField()

    class Meta:
        model = TermsOfUseFiles
        fields = ('terms_of_use_user', 'terms_of_use_site', 'map_site',)

    def get_map_site(self, obj):
        return config.map_site


class AffiliateSerializer(serializers.ModelSerializer):
    logo = FileSerializer()
    main_photo = FileSerializer()
    director = DirectorSerializer()
    social_networks = SocialNetworksSerializer(many=True)
    employees = EmployeeSerializer(many=True)
    partners = PartnerSerializer(many=True)
    about = FixAbsolutePathCkEditorSerializer()
    terms_of_use = serializers.SerializerMethodField()
    domens = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = (
            'id', 'created_at', 'name', 'company_name', 'slug', 'logo', 'main_photo',
            'phone_up', 'phone_down', 'email', 'city', 'address', 'copyright',
            'address_storage', 'domens', 'theme', 'about', 'terms_of_use',
            'social_networks', 'director', 'employees', 'partners',
        )
        read_only_fields = ('id', 'created_at',)

    @swagger_serializer_method(serializer_or_field=TermsOfUseSerializer())
    def get_terms_of_use(self, obj):
        if hasattr(obj, 'terms_of_use'):
            serializer = TermsOfUseSerializer(obj.terms_of_use, context=self.context)
            return serializer.data
        return None

    @swagger_serializer_method(serializer_or_field=serializers.ListField(child=serializers.CharField()))
    def get_domens(self, obj):
        if obj.domens:
            return obj.domens.split(',')
        return None


class AffiliateSlugsSerializer(serializers.ModelSerializer):
    domens = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = ('slug', 'domens', 'theme',)
        read_only_fields = ('id', 'created_at',)

    @swagger_serializer_method(serializer_or_field=serializers.ListField(child=serializers.CharField()))
    def get_domens(self, obj):
        if obj.domens:
            return obj.domens.split(',')
        return None


class AffiliateContactsSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)
    partners = PartnerSerializer(many=True)
    domen = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = (
            'phone_up', 'phone_down', 'email', 'domen', 'city', 'company_name',
            'address', 'work_graphic_office', 'work_graphic_storage', 'address_storage', 'latitude', 'longitude',
            'latitude_storage', 'longitude_storage', 'employees', 'partners',
        )
        read_only_fields = ('id', 'created_at',)

    def get_domen(self, obj):
        if obj.domens:
            return obj.domens.split(',')[0]
        return None


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = ('id', 'created_at', 'name_requisite', 'full_name', 'legal_address',
                  'physical_address', 'ogrn', 'inn', 'kpp', 'okpo', 'okved', 'okato',
                  'oktmo', 'okfc', 'payment_account', 'correspondent_account', 'bik')
