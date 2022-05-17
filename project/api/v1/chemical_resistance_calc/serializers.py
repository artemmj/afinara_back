import re

from rest_framework import serializers, exceptions

from phonenumber_field import validators

from apps.chemical_resistance_calc.models import (
    TableOfChemicalResistance, CalculatorCalculationRequest,
)


class TableOfChemicalResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = (
            'id', 'name', 'formula', 'state', 'concentration', 'temperature',
            'pvh', 'pp', 'pvdf', 'hpvh', 'nbr', 'epdm', 'fmk', 'ptfe',
        )
        read_only_fields = ('id',)


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = ('id', 'name', 'formula',)
        read_only_fields = ('id',)


class CalcStateRequestSerializer(serializers.Serializer):
    environment = serializers.CharField(required=True)


class CalcStateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = ('id', 'name', 'formula', 'state',)
        read_only_fields = ('id',)


class CalcConcentrateRequestSerializer(serializers.Serializer):
    environment = serializers.CharField(required=True)
    state = serializers.CharField(required=True)


class CalcConcentrateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = ('id', 'concentration',)
        read_only_fields = ('id',)


class CalcTemperatureRequestSerializer(serializers.Serializer):
    environment = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    concentration = serializers.CharField(required=True)


class CalcTemperatureResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = ('id', 'temperature',)
        read_only_fields = ('id',)


class CalcResultRequestSerializer(serializers.Serializer):
    environment = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    concentration = serializers.CharField(required=True)
    temperature = serializers.IntegerField(required=True)


class CalcResultResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOfChemicalResistance
        fields = (
            'id', 'pvh', 'pp', 'pvdf', 'hpvh', 'nbr', 'epdm', 'fmk', 'ptfe',
        )
        read_only_fields = ('id',)


class CalculateCalculatorRequestRequestSerializer(serializers.ModelSerializer):
    chemical_resistance = serializers.PrimaryKeyRelatedField(
        queryset=TableOfChemicalResistance.objects.all()
    )

    class Meta:
        model = CalculatorCalculationRequest
        fields = ('id', 'name', 'mail_or_phone', 'chemical_resistance',)

    def validate_mail_or_phone(self, value):
        try:
            validators.validate_international_phonenumber(value)
        except Exception:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                raise exceptions.ValidationError({'error': 'Введенный номер телефона / почта некорректны'})
        return value


class CalculateCalculatorRequestResponseSerializer(serializers.ModelSerializer):
    chemical_resistance = TableOfChemicalResistanceSerializer()

    class Meta:
        model = CalculatorCalculationRequest
        fields = ('id', 'name', 'mail_or_phone', 'chemical_resistance',)
