import logging

from apps import app
from .assortment_loader.loader import AssortmentXlsxLoader


logger = logging.getLogger('django_info')


@app.task()
def load_catalog_assortment(file_dest: str, catalog_id: str, price_files=None, images_file=None) -> str:
    AssortmentXlsxLoader(file_dest, catalog_id, pric_files=price_files, imgs_file=images_file).load()
    return 'Загрузка ассортимента успешно завершена.'
