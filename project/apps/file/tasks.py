import shutil

from apps import app
from django.conf import settings


@app.task()
def clear_pdf_files_dir():
    shutil.rmtree(f'{settings.MEDIA_ROOT}/pdf_files')
    return
