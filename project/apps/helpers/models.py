import uuid

from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django_lifecycle import LifecycleModel, hook

from .managers import DeletedManager, UserDeletedManager
from .services import transliterate


def get_next_value(name):
    with connection.cursor() as cursor:
        cursor.execute(f"select nextval('{name}');")
        row = cursor.fetchone()
    return row[0]


def get_or_repair_or_create(model, *args, **kwargs):
    obj, _ = model.objects.get_or_create(*args, **kwargs)
    if obj.deleted_at:
        obj.deleted_at = None
        obj.save()
    return obj


def get_or_repair_or_update(model, *args, **kwargs):
    obj, _ = model.objects.update_or_create(*args, **kwargs)
    if obj.deleted_at:
        obj.deleted_at = None
        obj.save()
    return obj


class ForceCleanModel(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    deleted_at = models.DateTimeField(_('deleted at'), db_index=True, null=True, blank=True, editable=False)

    objects = DeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class UserDeletedModel(models.Model):
    deleted_at = models.DateTimeField(_('deleted at'), db_index=True, null=True, blank=True, editable=False)

    objects = UserDeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class SLUGModel(LifecycleModel):
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract = True

    def create_update_slug(self, obj):
        solutions = self.__class__.objects.filter(name=obj.name).order_by('slug')
        if solutions:
            if len(solutions) == 1:
                self.slug = f'{transliterate(obj.name).lower()}-1'
            else:
                slug_number = int(solutions.last().slug.split('-')[-1])
                self.slug = f'{transliterate(obj.name).lower()}-{slug_number + 1}'
        else:
            self.slug = f'{transliterate(obj.name).lower()}'

    @hook('before_create')
    def create_slug_before_create(self):
        self.create_update_slug(self)

    @hook('before_update', when='name', has_changed=True)
    def update_slug_before_update(self):
        self.create_update_slug(self)
