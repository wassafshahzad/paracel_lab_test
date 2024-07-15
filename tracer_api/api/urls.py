from django.urls import path
from api.views import ping


urlpatterns = [
    path("ping/", ping)
]
