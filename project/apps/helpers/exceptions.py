from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import serializers, exceptions
from rest_framework.views import exception_handler as base_exception_handler


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    errors_text = serializers.CharField()
    errors = serializers.ListField()


def exception_handler(exc, context):
    response = base_exception_handler(exc, context)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if response is not None:
        data = {
            'status_code': exc.status_code,
            'errors_text': list(),
            'errors': {},
        }
        data['errors'] = exc.detail

        # Сформировать удобочитаемую строку для вывода пользователю
        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if isinstance(value, list):
                    # NOTE: Необходимо перевести на русский ключи некоторых ошибок
                    if key == 'fio':
                        key = 'ФИО'
                    elif key == 'email':
                        key = 'Электронная почта'
                    elif key == 'phone':
                        key = 'Номер телефона'
                    data['errors_text'].append(f'{key}: {value[0]}')
                elif isinstance(value, dict):
                    for _key, _value in value.items():
                        data['errors_text'].append(f'{key}.{_key}: {_value}')
        else:
            data['errors_text'].append(str(exc.detail))

        response.data = data
    return response
