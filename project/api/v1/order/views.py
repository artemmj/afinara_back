from rest_framework import permissions

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.order.models import Order
from .serializers import OrderSerializer


class OrderViewSet(ExtendedModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)
