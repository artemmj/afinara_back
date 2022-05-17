import logging

from django.conf import settings
from django.core.files import File as django_file

from apps.catalog.models import SizeChart, Product, ProdAttr, Attribute
from apps.file.models import File
from apps.support.models import Catalog as support_catalog

logger = logging.getLogger('django_info')


def set_attributes(attrs: list, product: Product) -> None:
    """ Устанавливает атрибуты/фильтры для продукта. """
    ProdAttr.objects.filter(product__vendor_code=product.vendor_code).delete()
    for data in attrs:
        if data[0].type == Attribute.AttrTypes.FLOAT:
            ProdAttr.objects.create(
                attribute=data[0], product=product, numeric=data[1]
            )
        elif data[0].type == Attribute.AttrTypes.CHAR:
            ProdAttr.objects.create(
                attribute=data[0], product=product, text=data[1]
            )


def set_size_chart(size_chart: str, product: Product) -> None:
    """ Устанавливает размерную таблицу для продукта. """
    try:
        datas = eval(size_chart)
    except Exception as exc:
        logger.info(f'Ошибка eval()! {exc} ({size_chart})')
        return

    SizeChart.objects.filter(product=product).delete()
    # Значения представлены как массив массивов, в строке
    # (по два элемента в каждом, название-характеристика)
    for data in datas:
        if data[0] and data[1]:
            SizeChart.objects.create(
                product=product,
                title=data[0],
                value=data[1],
            )


def load_image_into_product(imagenames: str, product: Product) -> None:
    """ Загружает картинки, если такие имеются, в продукт. """
    product.photos.all().delete(force=True)  # ?
    list_image_names = imagenames.split(',')
    jpeg_filenames_list = list()

    for image_name in list_image_names:
        try:
            splitted = image_name.split('.')
            name = '.'.join(splitted[:-1])
            ext = splitted[-1]
            if ext in ['eps', 'tif']:
                ext = 'jpg'
            jpeg_filenames_list.append((f'{name}.{ext}', f'{name.lower()}.{ext}', f'{name.upper()}.{ext}'))
        except ValueError as exc:
            logger.info(f'Ошибка при обработке изображения ({product.vendor_code}): {exc}')
            break

    for names in jpeg_filenames_list:
        ffile = None
        for filename in names:
            try:
                ffile = open(f'{settings.MEDIA_ROOT}/assortment/images/{filename}', 'rb+')
                break
            except FileNotFoundError:
                continue

        if not ffile:
            # logger.info(f'Не найден файл {jpeg_filenames_list}')
            continue
        else:
            corrfile = django_file(ffile)
            corrfile.name = corrfile.name.split('/')[-1]
            dbfile = File(file=corrfile)
            dbfile.save()
            product.photos.add(dbfile)
            product.save()
            ffile.close()
    return


def set_support_catalogs_to_product(support_catalogs_row: str, product: Product):
    """ Устанавливает для продукта связь с файлами-каталогами саппорта. """
    supp_catalogs = support_catalog.objects.filter(slug__in=support_catalogs_row.split(','))
    for sp in supp_catalogs:
        product.support_catalogs.add(sp)
        product.save()


def get_measure_for_product(name: str) -> str:
    """ Функция возвращает меру продукта (шт. или м.) в зависимости от названия.
    """
    if 'труба' in name.lower():
        return 'м.'

    return 'шт.'
