from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order,OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Category
        fields=['id','slug','title']
          
    
    
class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category',write_only=True)
    
    class Meta:
        model=MenuItem
        fields=['id','title','price','featured','category','category_id']
        
        

class CartSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=serializers.CurrentUserDefault())
    
    def validate(self, attrs):
        attrs['price']=attrs['unit_price'] * attrs['quantity']
        return attrs
   
    
    class Meta:
        model=Cart
        fields=['id','user','menuitem','quantity','unit_price','price']
        extra_kwargs = {
            'price': {'read_only': True}
        }
    
       
class OrderSerializer(serializers.ModelSerializer):

    
    class Meta:
        model=Order
        fields=['id','user','delivery_crew','status','total','date']   

               
        
class OrderItemSerializer(serializers.ModelSerializer):
    
     
    class Meta:
        model=OrderItem
        fields=['id','order','menuitem','quantity','unit_price','price']
        
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','email']
        
# -------------------------------------------------------------------------------------------------------------------------------------------------
        
