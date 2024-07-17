from django.urls import path
from api.views import ping, ListOrderAPIView, ListOrderItemsAPIView, RetrieveOrderAPIView


urlpatterns = [
    path("ping/", ping),
    path("order_items/", ListOrderItemsAPIView.as_view()),
    path("orders/", ListOrderAPIView.as_view(), name="orders-list"),
    path("orders/<str:tracking_number>/", RetrieveOrderAPIView.as_view(), name="orders-detail"),
]
