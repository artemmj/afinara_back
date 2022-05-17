from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .celery.views import CeleryResultView
from .ext.views import HealthView

from .chemical_resistance_calc.views import ChemicalResistanceCalcViewSet
from .questionnaires.views import QuestionnairesViewSet, QuestionnaireResultViewSet
from .seo.views import SeoViewSet
from .file.views import FileViewSet
from .pages.views import SolutionForAreaViewSet, AboutProductionViewSet
from .affiliates.views import AffiliatesViewSet
from .support.views import (
    ArticleViewSet, ArticleCategoriesViewSet, SupportCatalogViewSet,
    CatalogCategoriesViewSet, CertificateViewSet,
)
from .mailing_list.views import MailRecipientViewSet
from .catalog.views import CatalogViewSet, ProductViewSet, FilterViewSet
from .cart.views import CartViewSet
from .search.views import SearchViewSet
from .order.views import OrderViewSet
from .application.views import ApplicationViewSet

router = routers.DefaultRouter()
router.register(r'calculator', ChemicalResistanceCalcViewSet, basename='calculator')
router.register(r'seo', SeoViewSet, basename='seo')
router.register(r'questionnaires', QuestionnairesViewSet, basename='questionnaires')
router.register(r'questionnaires-results', QuestionnaireResultViewSet, basename='questionnaires-results')
router.register(r'file', FileViewSet, basename='file')
router.register(r'solutions-for-area', SolutionForAreaViewSet, basename='solutions-for-area')
router.register(r'affiliates', AffiliatesViewSet, basename='affiliates')
router.register(r'support/articles/categories', ArticleCategoriesViewSet, basename='support/articles/categories')
router.register(r'support/articles', ArticleViewSet, basename='support/articles')
router.register(r'support/catalogs/categories', CatalogCategoriesViewSet, basename='support/catalogs/categories')
router.register(r'support/catalogs', SupportCatalogViewSet, basename='support/catalogs')
router.register(r'support/certificates', CertificateViewSet, basename='support/certificates')
router.register(r'about-productions', AboutProductionViewSet, basename='about-productions')
router.register(r'mail-recipients', MailRecipientViewSet, basename='mail-recipients')
router.register(r'catalog/products', ProductViewSet, basename='catalog/products')
router.register(r'catalog/filters', FilterViewSet, basename='catalog/filters')
router.register(r'catalog', CatalogViewSet, basename='catalog')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'application', ApplicationViewSet, basename='application')

schema_view = get_schema_view(
    openapi.Info(
        title='Afinara project API',
        default_version='v1',
        description='Routes of Afinara project',
    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(<str:format>.json|.yaml)/', schema_view.without_ui(), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('', include((router.urls, 'api-root')), name='api-root'),
    path('celery/result/<pk>/', CeleryResultView.as_view()),
    path('health/', HealthView.as_view()),
]
