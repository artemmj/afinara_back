from django.core.management.base import BaseCommand
from apps.catalog.models import ProdAttr
from apps.helpers.services import transliterate

class Command(BaseCommand):
    def handle(self, **options):
        prod_attrs = ProdAttr.objects.all()

        for e in prod_attrs:
            if e.text_translit is None:
                e.text_translit = transliterate(e.text)
                e.save()
        print("Обработка завершена", flush=True)
