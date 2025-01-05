from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics
from .models import Category,MenuItem,Cart,Order,OrderItem
from .serializer import CategorySerializer,MenuItemSerializer,CartSerializer,OrderSerializer,OrderItemSerializer,UserSerializer
from django.contrib.auth.models import User, Group



from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permission import IsDeliveryCrew,IsManager
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from decimal import Decimal
from django.shortcuts import render, get_object_or_404



# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    
    def get_permissions(self):
        permission_classes = []
        
        if self.request.method!= 'GET':
            permission_classes=[IsAuthenticated]
        
        return[permission() for permission in permission_classes]
    
    
class  SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    def get_permissions(self):
        permission_classes=[]
        
        if self.request.method != 'GET':
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    

    
    
class MenuItemView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    
    search_fields = ['title', 'category__title']
    ordering_fields = ['price']
    
    def get_permissions(self):
        permission_classes=[]
        if self.request.method != 'GET':
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    
    def get_permissions(self):
        permission_classes=[]
        if self.request.method != 'GET':
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    



class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    
    def get_queryset(self,*args,**kwargs):
        
        return Cart.objects.all().filter(user=self.request.user)
    
    def delete(self,*args,**kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return ({'Deleted cart'})
    
    permission_classes=[IsAuthenticated]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    

    

        
   

class OrderView(generics.ListCreateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    def get_queryset(self,*args,**kwargs):
        
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.filter(name='Delivery crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        elif self.request.user.groups.count() == 0:
            return Order.objects.all().filter(user=self.request.user)
        else:
            return Order.objects.all()
    
    
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(menuitem=cart_item.menuitem, quantity=cart_item.quantity,
                                     unit_price=cart_item.unit_price, price=cart_item.price, order=order)
            cart_item.delete()



    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total
    
    
    
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count() == 0:
            return Response('Empty ')
        else:
            return super().update(request, *args, **kwargs)
    
    


class DeliveryCrewView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes = [IsManager]
    
    def get_queryset(self):
        delivery_group=Group.objects.get(name='Delivery crew')
        queryset=User.objects.filter(groups=delivery_group)
        return queryset
    
    
    def perform_create(self, serializer):
        
        delivery_group=Group.objects.get(name='Delivery crew')
        user=serializer.save()
        user.groups.add(delivery_group)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView) :
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes = [IsManager]
    
    def get_queryset(self):
        delivery_group=Group.objects.get(name='Delivery crew')
        queryset=User.objects.filter(groups=delivery_group)
        return queryset  
    
    def delete(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew_group = Group.objects.get(name='delivery crew')
            delivery_crew_group.user_set.remove(user)
            return Response({'Message':'User had been removed.'}, status.HTTP_200_OK)
        return Response({'Message':'Error.'}, status.HTTP_404_NOT_FOUND)
    
    permission_classes = [IsAuthenticated]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    
    
    
    
class ManagerView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes = [IsAdminUser]
    ##
    
    def get_queryset(self):
        manager_group=Group.objects.get(name='Manager')
        queryset=User.objects.filter(groups=manager_group)
        return queryset
    
    def perform_create(self, serializer):
        
        manager_group=Group.objects.get(name='Manager')
        user=serializer.save()
        user.groups.add(manager_group)
        
    permission_classes=[IsManager]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
        

class SingleManagerView(generics.RetrieveDestroyAPIView):
    serializer_class=UserSerializer
    
    def get_queryset(self):
        manager_group=Group.objects.get(name='Manager')
        queryset=User.objects.filter(groups=manager_group)
        return queryset
    
    
    def delete(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.remove(user)
            return Response({'Message':'User had been removed.'}, status.HTTP_200_OK)
        return Response({'Message':'Error.'}, status.HTTP_404_NOT_FOUND)
    
    
    permission_classes=[IsManager]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    
    
 