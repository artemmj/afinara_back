import logging
import csv
import xlrd
import os
import zipfile
import shutil
import uuid

from django.db import transaction
from django.conf import settings

from apps.catalog.models import Product, Catalog, Attribute
from .helpers import (
    set_attributes, set_size_chart, load_image_into_product,
    set_support_catalogs_to_product, get_measure_for_product,
)

logger = logging.getLogger('django_info')


class AssortmentXlsxLoader():
    def __init__(self, file_dest, catalog_id, pric_files=None, imgs_file=None):
        self.file_dest = file_dest
        self.catalog = Catalog.objects.get(pk=catalog_id)
        self.subcatalog = None
        self.price_files_dests = pric_files if pric_files else None
        self.images_file_dest = imgs_file if imgs_file else None

    @transaction.atomic
    def process_worksheets(self, csvdests: list):
        ''' Ф-ция обрабатывает листы, каждый файл csv - лист. '''
        for csvdest, catalog in csvdests:
            rows_dict = list()
            with open(csvdest) as File:
                reader = csv.DictReader(File)
                for row in reader:
                    rows_dict.append(row)

            for row in rows_dict:
                prodattrs = list()
                correct_row = dict()
                # Обрезать пробелы, могут встречаться.
                for key, value in row.items():
                    correct_row[key.strip()] = value.strip()

                vendor_code = correct_row.pop('Артикул')
                if not vendor_code or vendor_code == '':
                    logger.info(f'Товар с путым артикулом! row: {correct_row}')
                    continue

                description_text = correct_row.pop('Вводный текст')
                name = correct_row.pop('Краткое наименование')
                fullname = correct_row.pop('Полное наименование')
                imagenames = correct_row.pop('Картинка', None)
                size_chart = correct_row.pop('Размерный ряд', None)
                support_catalogs_row = correct_row.pop('Каталоги', None)

                if '' in correct_row:
                    del correct_row['']
                if None in correct_row:
                    del correct_row[None]

                for colname, value in correct_row.items():
                    # Динамические атрибуты товаров.
                    # TODO После корректировки файлов, проставить
                    # динамическое определение типа, пока что все char.
                    if value:
                        attribute, _ = Attribute.objects.get_or_create(
                            name=colname,
                            type=Attribute.AttrTypes.CHAR
                        )
                        attribute.save()
                        prodattrs.append((attribute, value))

                product, _ = Product.objects.update_or_create(
                    catalog=catalog,
                    vendor_code=vendor_code,
                    defaults={
                        'name': name,
                        'full_name': fullname,
                        'description_text': description_text,
                        'measure': get_measure_for_product(name),
                    }
                )
                set_attributes(prodattrs, product)

                if imagenames:
                    load_image_into_product(imagenames, product)

                if size_chart:
                    set_size_chart(size_chart, product)

                if support_catalogs_row:
                    set_support_catalogs_to_product(support_catalogs_row, product)

    @transaction.atomic
    def process_price_files(self):
        ''' Функция обрабатывает файл/ы цен, если есть. '''
        if self.price_files_dests:
            csv_price_files = list()
            for filedest in self.price_files_dests:
                workbook = xlrd.open_workbook(filedest)
                sheet = workbook.sheet_by_index(0)
                csvname = f'{filedest.split("/")[-1].split(".")[0]}_цены.csv'
                csvdest = f'{settings.MEDIA_ROOT}/assortment/{csvname}'
                outcsv = open(csvdest, 'w')
                csvwriter = csv.writer(outcsv, quoting=csv.QUOTE_ALL)
                for rownumber in range(sheet.nrows):
                    csvwriter.writerow(sheet.row_values(rownumber))
                outcsv.close()
                csv_price_files.append(csvdest)

            for csvfile_dest in csv_price_files:
                rows_dict = list()
                with open(csvfile_dest) as File:
                    reader = csv.DictReader(File)
                    for row in reader:
                        rows_dict.append(row)
                for row in rows_dict:
                    try:
                        product = Product.objects.get(vendor_code=row['Артикул'])
                        product.price = row['Цена']
                        product.save()
                    except Product.DoesNotExist:
                        logger.info(f'Не найден товар с артикулом {row["Артикул"]}')
                    except Exception as exc:
                        logger.info(f'При загрузке произошла ошибка: {exc}')

    def load(self):
        ''' Точка входа, загрузка файла. Перегоняем в csv, т.к.
        openpyxl непозволительно долго обрабатывает файл.
        '''
        def create_csv_file_from_sheet(sheet):
            ''' Вспомогательная функция для конвертации xlsx в csv. '''
            excelname = self.file_dest.split('/')[-1]
            csvname = f'{excelname.split(".")[0]}_{uuid.uuid4()}.csv'
            csvdest = f'{settings.MEDIA_ROOT}/assortment/{csvname}'
            outcsv = open(csvdest, 'w')
            csvwriter = csv.writer(outcsv, quoting=csv.QUOTE_ALL)
            for rownumber in range(sheet.nrows):
                csvwriter.writerow(sheet.row_values(rownumber))
            outcsv.close()
            return csvdest

        workbook = xlrd.open_workbook(self.file_dest)
        csv_dests = list()
        sheetnames = workbook.sheet_names()
        if len(sheetnames) == 1:
            self.subcatalog = self.catalog
            sheet = workbook.sheet_by_name(sheetnames[0])
            csvdest = create_csv_file_from_sheet(sheet)
            csv_dests.append((csvdest, self.subcatalog))
        else:
            for sheetname in sheetnames:
                self.subcatalog, _ = Catalog.objects.get_or_create(
                    name=sheetname,
                    parent=self.catalog
                )
                sheet = workbook.sheet_by_name(sheetname)
                csvdest = create_csv_file_from_sheet(sheet)
                csv_dests.append((csvdest, self.subcatalog))

        if self.images_file_dest:
            # Тут важно приготовить каталог для картинок (создать и
            # распаковать архив изображений) перед вызовом process_worksheets()
            imgs_dir = f'{settings.MEDIA_ROOT}/assortment/images'
            if not os.path.exists(imgs_dir):
                os.mkdir(imgs_dir)
            with zipfile.ZipFile(self.images_file_dest, 'r') as zip_ref:
                zip_ref.extractall(imgs_dir)

        self.process_worksheets(csv_dests)
        self.process_price_files()
        shutil.rmtree(f'{settings.MEDIA_ROOT}/assortment')
