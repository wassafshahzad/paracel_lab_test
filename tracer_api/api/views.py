
from django.db.models.query import QuerySet

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.models import OrderItem, OrderModel
from api.serializers import OrderItemSerializer, OrderSerializer

@api_view()
def ping(_):
    return Response({"message": "Pong"})


class ListOrderItemsAPIView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ListOrderAPIView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        carrier = self.kwargs.get("carrier", None)
        if carrier:
            return OrderModel.objects.filter(carrier__name = carrier)
        return  OrderModel.objects.all()
    

class RetrieveOrderAPIView(RetrieveAPIView):
    queryset = OrderModel.objects.all()
    lookup_field = "tracking_number"
    serializer_class = OrderSerializer