from django import forms
from django.core.exceptions import ValidationError


class LoadAssortmentForm(forms.Form):
    assortment_file = forms.FileField(label='Файл ассортимента')
    price_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label='Файлы цен',
    )
    images_file = forms.FileField(required=False, label='Архив изображений')

    def clean(self):
        cleaned_data = super().clean()
        assortment_filename = cleaned_data['assortment_file'].name
        images_filename = cleaned_data['images_file'].name if cleaned_data['images_file'] else None
        # price_files = cleaned_data['price_files'] if cleaned_data['price_files'] else None

        errors = list()
        if assortment_filename.split('.')[-1] != 'xlsx':
            errors.append('Для файла ассортимента доступен только формат xlsx!')

        if images_filename and images_filename.split('.')[-1] != 'zip':
            errors.append('Для файла архива изображений доступен только формат zip!')

        # TODO Валидация списка файлов цен

        if errors:
            raise ValidationError(errors)
