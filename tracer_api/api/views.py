from django.db.models.query import QuerySet

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.models import OrderItem, OrderModel
from api.serializers import OrderItemSerializer, OrderSerializer


@api_view()
def ping(_):
    return Response({"message": "Pong"})


class ListOrderItemsAPIView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    @extend_schema(
        description="Retrieve a list of OrderItem instances.",
        responses={200: OrderItemSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListOrderAPIView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        carrier = self.kwargs.get("carrier", None)
        filters = {}

        carrier = self.request.query_params.get("carrier", None)
        tracking_number = self.request.query_params.get("tracking_number", None)

        if carrier:
            filters["carrier"] = carrier
        if tracking_number:
            filters["tracking_number"] = tracking_number

        return OrderModel.objects.filter(**filters)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="carrier",
                description="Filter by carriers",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="tracking_number",
                type=str,
                description="Filter by tracking number.",
            ),
        ],
        description="Retrieve a List of deliveries, \
        This endpoint does allow filtering on the basis of carrier and tracking_number.",
        responses={200: OrderSerializer(many=True)},
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class RetrieveOrderAPIView(RetrieveAPIView):
    queryset = OrderModel.objects.all()
    lookup_field = "tracking_number"
    serializer_class = OrderSerializer


    @extend_schema(
        description="Retrieve a delivery based on the tracking number.",
        responses={200: OrderSerializer(many=True)},    
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
