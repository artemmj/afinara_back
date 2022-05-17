from django.shortcuts import get_object_or_404

from rest_framework.request import Request

from apps.catalog.models import Product
from .generate_pdf_from_html import generate_pdf_file_from_html
from ..serializers import ProductDetailSerializer


def _get_headers_for_table(elem: dict) -> list:
    """ Функция наполняет массив строками-заголовками таблицы.
    """
    headers = []
    elem.pop('id')
    for key in elem.keys():
        if key == 'name' and elem[key]:
            headers.append('Наименование')
        elif key == 'vendor_code' and elem[key]:
            headers.append('Артикул')
        elif key == 'price' and elem[key]:
            headers.append('Цена')
        elif key == 'diameter' and elem[key]:
            headers.append('Диаметр')
        elif key == 'expand' and elem[key]:
            headers.append('Расход')
        elif key == 'seal_material' and elem[key]:
            headers.append('Материал уплотнения')
    return headers


def get_pdf_assortment_filepath(product_id: str, request: Request) -> str:
    """ Фукнция по переданному product_id генерирует pdf-файл
    с ассортиментом продукта, возвращает путь до него.
    """
    product = get_object_or_404(Product, pk=product_id)
    assortment: list = ProductDetailSerializer(product).data['assortment']
    headers = _get_headers_for_table(assortment[0].copy())

    html = """
<!DOCTYPE html>
<html>
<head>
<style>
@font-face {
    font-family: DejaVuSans;
    src: url("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf");
}
table, th, td {
    border: 1px solid black;
    padding: 3px;
    font-family: DejaVuSans;
}
table {
    width: 100%;
    font-family: DejaVuSans;
}
</style>
</head>
<body>
<table class="table">
<thead>
<tr>
"""
    # Вывести заголовки
    for header in headers:
        html += f'\t<th>{header}</th>\n'
    html += '</tr>\n</thead>\n<tbody>\n'

    # Вывести элементы
    for row in assortment:
        row.pop('id')
        html += '\t<tr>\n'
        for cell in row.values():
            if cell:
                html += f'\t\t<td>{cell}</td>\n'
        html += '\t</tr>'
    html += '</tbody></table></body></html>'

    return generate_pdf_file_from_html(html, request)
