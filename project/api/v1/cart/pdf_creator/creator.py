import os
import uuid
import logging
from datetime import datetime

from django.conf import settings
from django.core.files import File as django_file

from xhtml2pdf import pisa

from apps.file.models import File

logger = logging.getLogger('django_errors')


def create_pdf_cart(cart, context) -> str:
    ''' Функция генерирует pdf-файл с содержимым переданной корзины. '''

    upper_html = """
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
p {
    font-family: DejaVuSans;
}
</style>
</head>
<body>""" + f"<p>Ваш заказ от {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>" + """<table>
<tr>
    <th width=60>Изображение</th>
    <th width=75>Артикул</th>
    <th width=280>Наименование позиции</th>
    <th width=30>Кол-во</th>
    <th width=50>Единица</th>
    <th width=35>Цена</th>
</tr>"""

    lower_html = f'</table><p align="right">Итого: {cart.total_amount()}</p></body></html>'

    cart_products = cart.cart_products.all()
    middle_html = ''
    for cart_product in cart_products:
        if cart_product.product.photos.first():
            path = cart_product.product.photos.first().file.path
            middle_html += f'<tr><td><img border=3 height=30px width=30px src="{path}"></img></td>'
        else:
            middle_html += '<tr><td>Нет изображения</td>'

        product_price = cart_product.product.price
        middle_html += f'<td>{cart_product.product.vendor_code}</td>'\
            f'<td>{cart_product.product.name}</td>'\
            f'<td>{cart_product.count}</td>'\
            f'<td>{cart_product.product.measure}</td>'\
            f'<td>{product_price if product_price else "н/д"}</td></tr>'

    full_html = upper_html + middle_html + lower_html

    if not os.path.exists(f'{settings.MEDIA_ROOT}/pdf_carts'):
        os.mkdir(f'{settings.MEDIA_ROOT}/pdf_carts')
    output_dest = f'{settings.MEDIA_ROOT}/pdf_carts/{uuid.uuid4()}.pdf'

    with open(output_dest, 'wb+') as ofile:
        pisa_status = pisa.CreatePDF(full_html, ofile)

    if pisa_status.err:
        logger.error(pisa_status.err)

    with open(output_dest, 'rb+') as ifile:
        corrfile = django_file(ifile)
        fileobj = File(file=corrfile)
        request = context['request']
        absurl = request.build_absolute_uri(fileobj.file.path)

    return absurl
