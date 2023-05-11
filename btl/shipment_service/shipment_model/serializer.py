from rest_framework import serializers
from .models import Shipment,TypeShipment


class TypeShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeShipment
        fields = '__all__'
class ShipmentSerializer(serializers.ModelSerializer):
    type_shipment = TypeShipmentSerializer(read_only=True, many=False)
    class Meta:
        model = Shipment
        fields = '__all__'