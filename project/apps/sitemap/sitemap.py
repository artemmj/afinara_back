from django.contrib.sitemaps import Sitemap
from apps.pages.models import SolutionForArea, AboutProduction
from apps.affiliates.models import Affiliate
from apps.catalog.models import Catalog, Product
from datetime import datetime


class SolutionForAreaViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return SolutionForArea.objects.all()

    def location(self, item):
        return f'/solution/{item.slug}'

    def lastmod(self, item):
        return datetime.now()


class CatalogViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Catalog.objects.all()

    def location(self, item):
        if item.parent:
            return f'/catalog/{item.parent.slug}/{item.slug}'
        return f'/catalog/{item.slug}'

    def lastmod(self, item):
        return item.created_at


class AboutProductionViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return AboutProduction.objects.all()

    def location(self, item):
        return f'/information/{item.slug}'


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['/solutions', '/information', '/catalog', '/product', '/contacts']

    def location(self, item):
        return item



class ProductViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def location(self, item):
        if item.catalog.parent:
            return f'/catalog/{item.catalog.parent.slug}/{item.catalog.slug}/{item.pk}'
        return f'/catalog/{item.catalog.slug}/{item.catalog.slug}/{item.pk}'

    def lastmod(self, item):
        return item.created_at


class MainViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['']

    def location(self, item):
        return item
