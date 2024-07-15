from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from api.utils import generate_tracking_numbers

class BaseModel(models.Model):
    """Base model having timestamp fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: True


class AddressModel(BaseModel):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", blank=True, null=True
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return human readable representation.

        Returns:
            str: A string with human readable representation.
        """

        return f"{self.street}, {self.postal_code}, {self.city}, {self.country}"


class ArticleModel(BaseModel):

    sku = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()


class CarrierModel(models.Model):

    name = models.CharField(max_length=255, unique=True, primary_key=True)


class OrderModel(BaseModel):

    class Status(models.TextChoices):
        IN_TRANSIT = "in-transit"
        INBOUND_SCAN = "inbound-scan"
        DELIVERY = "delivery"
        TRANSIT = "transit"
        SCANNED = "scanned"

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_deliveries"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_deliveries"
    )
    scheduled_for   = models.DateTimeField()
    delivered_at    = models.DateTimeField(blank=True, null=True)
    status          = models.CharField(choices=Status.choices, default=Status.SCANNED, max_length=20)
    carrier         = models.ForeignKey(CarrierModel, on_delete=models.CASCADE, related_name="deliveries")
    tracking_number = models.CharField(max_length=50, unique=True, blank=True, null=True)


    def save(self, *args,  **kwargs) -> None:
        """Override save method to generate tracking number."""

        if not  self.tracking_number:
            self.tracking_number = generate_tracking_numbers()
        return super().save(*args,  **kwargs)


    def __str__(self):
        return f"Delivery from {self.sender.username} to {self.receiver.username} - Status: {self.status}"


class OrderItem(models.Model):

    articles = models.ForeignKey(
        ArticleModel,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["articles", "order"], name="unique Orders"
            )
        ]

