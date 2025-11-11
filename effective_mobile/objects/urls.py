from django.urls import path
from objects import api


urlpatterns = [
    path("products/", api.ProductListView.as_view(), name="products"),
    path("products/<int:id>", api.ProductDetailView.as_view(), name="product"),
    path("orders/", api.OrderListView.as_view(), name="orders"),
    path("orders/<int:id>/", api.OrderDetailView.as_view(), name="order"),
]