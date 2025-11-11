from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from objects.models import Order, Product
from objects.serializers import ProductSerializer, OrderSerializer

from users.jwt import get_user_data
from users.models import AccessRoleRule 


@extend_schema(tags=['Products'])
class ProductListView(ListAPIView):
    """API списка продуктов"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={'message': "Для просмотра продуктов необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        rules = get_object_or_404(AccessRoleRule, role=user.role)

        if not rules.read_all_permission and not user.role.name == "admin":
            return Response(
                data={'message': "У вас недосаточно прав"},
                status=status.HTTP_403_FORBIDDEN
            )

        return self.list(request, *args, **kwargs)


@extend_schema(tags=["Products"])
class ProductDetailView(RetrieveAPIView):
    """API конкретного продукта"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def retrieve(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={'message': "Для просмотра продукта необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        rules = get_object_or_404(AccessRoleRule, role=user.role)

        if not rules.read_exact_permission and not user.role.name == "admin":
            return Response(
                data={'message': "У вас недосаточно прав"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["Orders"])
class OrderListView(ListAPIView):
    """API списка заказов"""
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={'message': "Для просмотра заказов необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user.role.name == "admin":
            self.queryset = Order.objects.all()
        else:
            self.queryset = Order.objects.filter(owner=user)

        return self.list(request, *args, **kwargs)
    

@extend_schema(tags=["Orders"])
class OrderDetailView(RetrieveAPIView):
    """API конкретного заказа"""
    serializer_class = OrderSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = get_user_data(request)
        if not user:
            return Response(
                data={'message': "Для просмотра заказа необходимо войти"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        instance = self.get_object()
        if instance.owner != user and not user.role.name == "admin":
            return Response(
                data={'message': "У вас нет прав для просмотра данного заказа"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
