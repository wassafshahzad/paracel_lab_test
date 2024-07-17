from rest_framework import serializers

from api.models import OrderModel, OrderItem, ArticleModel
from api.utils import get_postal_city_country, get_cached_weather_data


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer class for Articles."""

    class Meta:
        model = ArticleModel
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer class for Order Items"""

    articles = ArticleSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ["articles", "quantity"]


class OrderSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(many=True)
    carrier = serializers.SlugRelatedField(
        slug_field="name", many=False, read_only=True
    )

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

    def to_representation(self, instance):

        instance = super().to_representation(instance)
        postal_code, country, _ = get_postal_city_country(instance.get("receiver"))

        data = get_cached_weather_data(f"{postal_code}_{country}")

        instance["temp"] = data.get("temp", "")
        instance["weather"] = data.get("weather", "")
        return instance


class WeatherSerializer(serializers.Serializer):
    temp = serializers.IntegerField()
    description = serializers.CharField(source="weather.description")

    class Meta:
        extra_kwargs = {"extra_field": {"required": False, "allow_blank": True}}
