from drf_yasg.utils import swagger_auto_schema
from api.v1.search.serializers import SearchQueryParamsSerializer
from apps.helpers.viewsets import ExtendedViewSet
from rest_framework.generics import GenericAPIView
from apps.helpers.viewsets import paginate_response
from api.v1.catalog.serializers import ProductSerializer
from apps.catalog.models import Product
from django.db.models import Q


class SearchViewSet(ExtendedViewSet, GenericAPIView):

    def get_queryset(self):
        query = self.request.query_params['query']
        return Product.objects.filter(Q(name__icontains=query) | Q(vendor_code__icontains=query) |
                                      Q(full_name__icontains=query))

    @swagger_auto_schema(query_serializer=SearchQueryParamsSerializer, responses={200: ProductSerializer})
    def list(self, request, *args, **kwargs):
        query_serializer = SearchQueryParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        return paginate_response(
            self,
            queryset,
            ProductSerializer,
            context={'request': request}
        )

