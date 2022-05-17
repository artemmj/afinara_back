from rest_framework.exceptions import APIException


class ServiceError(APIException):
    status_code = 400
    default_detail = 'Ошибка в работе сервиса'
    default_code = 'service_error'


class AbstractService:
    """Родитель всех сервисов, все сервисы в системе должны наследоваться от него"""

    def process(self, *args, **kwargs):
        raise NotImplementedError("Should implement this error")


def transliterate(string):
    """ Транслитерирует кириллическую строку. """
    dictionary = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'u', 'я': 'ya',  'А': 'A',
        'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH',
        'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'H', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '',
        'Ы': 'y', 'Ь': '', 'Э': 'E', 'Ю': 'U', 'Я': 'YA', ', ': '', '?': '',
        ' ': '_', '~': '', '!': '', '@': '', '#': '', '$': '', '%': '',
        '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
        ': ': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '',
        '/': '', '№': '', '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '',
        'є': '', 'Ґ': 'g', 'Ї': 'i', 'Є': 'e',  '—': '',
    }
    for key in dictionary:
        string = string.replace(key, dictionary[key])
    return string
