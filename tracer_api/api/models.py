from django.db import models
from django.core.validators import MinValueValidator

from api.utils import generate_tracking_numbers

class BaseModel(models.Model):
    """Base model having timestamp fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract= True


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

    sender = models.CharField(max_length=255, blank=False, null= False)

    receiver = models.CharField(max_length=255, blank=False, null= False)

    scheduled_for   = models.DateTimeField()
    delivered_at    = models.DateTimeField(blank=True, null=True)
    status          = models.CharField(choices=Status.choices, default=Status.SCANNED, max_length=20)
    carrier         = models.ForeignKey(CarrierModel, on_delete=models.CASCADE, related_name="deliveries")
    tracking_number = models.CharField(max_length=50, unique=True, blank=True, null=True)


    def save(self, *args,  **kwargs) -> None:
        """Override save method to generate tracking number."""

        if not self.tracking_number:
            self.tracking_number = generate_tracking_numbers()
        return super().save(*args,  **kwargs)


    def __str__(self):
        return f"Delivery from {self.sender} to {self.receiver} - Status: {self.status}"


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

