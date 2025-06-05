from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from order.models import Cart, CartItem,Order, OrderItem
from order.serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer, CartItemUpdateSerializers, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from order.services import OrderServices
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        if Cart.objects.filter(user=request.user).first():
            serializer = self.get_serializer(Cart.objects.filter(user=request.user).first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        elif self.request.method == 'PATCH':
            return CartItemUpdateSerializers
        return CartItemSerializer
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_pk'] = self.kwargs.get('cart_pk')
        return context
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete','head','option']
    
    @action(detail=True, methods=['post'])
    def cancel(self,request,pk=None):
        order = self.get_object()
        OrderServices.cancel_order(order=order, user=self.request.user)
        
        return Response({'status':'Order Canceled'})
    
    @action(detail=True, methods=['patch'])
    def update_satatus(self, request, pk=None):
        order  = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True, context=self.get_serializer_context())

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status" : f"Order status updated to {request.data['status']}"})
        
    
    
    def get_permissions(self):
        
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user':self.request.user}
    
    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        if self.request.method == "POST":
            return CreateOrderSerializer
        
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user = self.request.user)
        
