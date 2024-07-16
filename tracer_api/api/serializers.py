from rest_framework.serializers import ModelSerializer, SlugRelatedField

from api.models import OrderModel, OrderItem, ArticleModel


class ArticleSerializer(ModelSerializer):
    """Serializer class for Articles."""

    class Meta:
        model = ArticleModel
        fields = "__all__"


class OrderItemSerializer(ModelSerializer):
    """Serializer class for Order Items"""

    articles = ArticleSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ["articles", "quantity"]


class OrderSerializer(ModelSerializer):

    order_items = OrderItemSerializer(many=True)
    carrier  = SlugRelatedField(slug_field='name', many=False, read_only=True)

    class Meta:
        model = OrderModel
        fields = [
            "order_items",
            "sender",
            "receiver",
            "status",
            "carrier",
            "tracking_number",
        ]
