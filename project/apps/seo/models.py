from django.db import models

from apps.helpers.models import UUIDModel, CreatedModel


class Seo(UUIDModel, CreatedModel):
    name = models.CharField(max_length=256)
    route = models.TextField()
    title = models.TextField()
    h1 = models.TextField()
    description = models.TextField()
    keywords = models.TextField()
    canonical_rel = models.TextField()
    domain = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = 'seo'
        verbose_name_plural = 'seo'
