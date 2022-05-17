from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from apps.sitemap.sitemap import (MainViewSitemap,
                                  StaticViewSitemap,
                                  AboutProductionViewSitemap, SolutionForAreaViewSitemap,
                                  CatalogViewSitemap, ProductViewSitemap)
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'main': MainViewSitemap,
    'catalog': CatalogViewSitemap,
    'static': StaticViewSitemap,
    'aboutproduction': AboutProductionViewSitemap,
    'solutionforarea': SolutionForAreaViewSitemap,
    'product': ProductViewSitemap,

}

admin.site.site_title = 'Afinara'
admin.site.site_header = 'Afinara'
admin.site.index_title = 'Панель администрирования'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.v1.urls', 'api_v1'))),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url('^sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
