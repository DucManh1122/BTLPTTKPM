from rest_framework import serializers
from .models import Category,Product,StoreHouse,Suppliers


class StoreHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHouse
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    supplier = SuppliersSerializer(read_only=True, many=False)
    category = CategorySerializer(read_only=True, many=False)
    storehouse = StoreHouseSerializer(read_only=True, many=False)
    class Meta:
        model = Product
        fields = '__all__'  
