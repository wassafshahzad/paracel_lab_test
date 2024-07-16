from django.contrib import admin

from api.models import ArticleModel, OrderItem, OrderModel, CarrierModel


admin.site.register(ArticleModel)
admin.site.register(OrderItem)
admin.site.register(OrderModel)
admin.site.register(CarrierModel)
