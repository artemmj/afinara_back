import logging

from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from apps.catalog.models import Product
from .generate_pdf_from_html import generate_pdf_file_from_html
from ..serializers import ProductDetailSerializer

logger = logging.getLogger('django_info')


def _get_easy_data(size_chart: list) -> list:
    """ Функция преобразует сырой набор данных из БД в более удобный.
    """
    easy_data = []
    for row in size_chart:
        easy_dict = {'Артикул': row['vendor_code']}
        for character in row['size_chart']:
            easy_dict[character['title']] = character['value']
        easy_data.append(easy_dict)
    return easy_data


def make_size_chart_pdf(product_id: str, request: Request) -> str:
    """ Фукнция по переданному product_id генерирует pdf-файл
    с размерным рядом продукта, возвращает путь до него.
    """
    product = get_object_or_404(Product, pk=product_id)
    size_chart: list = ProductDetailSerializer(product).data['size_chart']
    easy_data = _get_easy_data(size_chart)

    photo = None
    # Подключить картинку, вторую, если есть
    photos = product.photos.all()
    if len(photos) > 1:
        photo = photos[1]
    elif len(photos) == 1:
        photo = photos[0]

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
.header img {
  float: left;
  width: 220px;
  background: #555;
}
.header h1 {
  position: relative;
  top: 100px;
  left: 100px;
  font-family: DejaVuSans;
}
</style>
</head>
<body>
""" + """
<div class="header">""" + f"""
    <img src="{photo.file.path if photo else None}" alt="logo" />""" + f"""
    <h1>{product.fullname_with_attrs}</h1>""" + """
</div>""" + """
<table class="table">
    <thead>
    <tr>
"""
    # Вывести заголовки
    for idx, header in enumerate(easy_data[0].keys()):
        if idx == 0:
            html += f'\t<th width=100>{header}</th>\n'
        else:
            html += f'\t<th>{header}</th>\n'
    html += '</tr>\n</thead>\n<tbody>\n'

    # Вывести элементы
    for row in easy_data:
        html += '\t<tr>\n'
        for cell in row.values():
            html += f'\n\t\t<td>{cell}</td>\n'
        html += '\t</tr>'
    html += '</tbody></table></body></html>'

    return generate_pdf_file_from_html(html, request)
