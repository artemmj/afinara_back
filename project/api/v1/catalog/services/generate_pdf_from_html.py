import os
import uuid
import logging

from django.conf import settings
from django.core.files import File as django_file
from rest_framework.request import Request

from xhtml2pdf import pisa

from apps.file.models import File

logger = logging.getLogger('django_errors')


def generate_pdf_file_from_html(html: str, request: Request) -> str:
    """ Функция генерирует pdf файл с таблицей
    из строки с html разметкой, возвращает путь до него.
    """
    if not os.path.exists(f'{settings.MEDIA_ROOT}/pdf_files'):
        os.mkdir(f'{settings.MEDIA_ROOT}/pdf_files')
    output_dest = f'{settings.MEDIA_ROOT}/pdf_files/{uuid.uuid4()}.pdf'

    with open(output_dest, 'wb+') as ofile:
        pisa_status = pisa.CreatePDF(html, ofile)

    if pisa_status.err:
        logger.error(pisa_status.err)

    with open(output_dest, 'rb+') as ifile:
        corrfile = django_file(ifile)
        fileobj = File(file=corrfile)
        absurl = request.build_absolute_uri(fileobj.file.path)

    return absurl
