CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "stylesheetparser",
        'allowedContent': True,
        'toolbar_Full': [
            [
                'Format', 'Bold', 'Italic', 'Subscript', 'Superscript',
                '-' 'Link', 'Unlink', '-', 'Link', 'Unlink', '-', 'Blockquote', '-',
            ],
            [
                'Image', 'Flash', 'Table', 'HorizontalRule',
            ],
            [
                'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
            ]
        ],
    }
}
