from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TypeShipment,Shipment
from .serializer import ShipmentSerializer,TypeShipmentSerializer
import requests
import json

# Create your views here.
@api_view(['GET','POST','PUT'])
def crud_type_shipment(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên bán hàng':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        name = request.data.get('Name')
        if not name: return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'name': name
        }
        serializer = TypeShipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên bán hàng':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        name = request.data.get('Name')
        if not (name and id): return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            type_shipmnet = TypeShipment.objects.get(id=id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy loại hình vận chuyển"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'id': id,
            'name': name
        }
        serializer = TypeShipmentSerializer(type_shipmnet,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = TypeShipment.objects.all()
            serializer = TypeShipmentSerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','PUT'])
def crud_shipment(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên bán hàng':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        id_type_shipment = request.data.get('Type Shipment ID')
        fromAddress = request.data.get('From')
        toAddress = request.data.get('To')
        
        if not (fromAddress and toAddress and id_type_shipment): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        try:
            type_shipment = TypeShipment.objects.get(id=id_type_shipment)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy loại hình vận chuyển"},status=status.HTTP_400_BAD_REQUEST)
        try:
            Shipment.objects.get(fromAddress=fromAddress,toAddress=toAddress,type_shipment=type_shipment)
            return Response({'status':'Failed','error': "Đã tồn tại shipment"},status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {
                'fromAddress': fromAddress,
                'toAddress': toAddress,
                'type_shipment': type_shipment,
            }
            serializer = ShipmentSerializer(data=data)
            if serializer.is_valid():
                serializer.create(data)
                return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên bán hàng' :
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        id_type_shipment = request.data.get('Type Shipment ID')
        fromAddress = request.data.get('From')
        toAddress = request.data.get('To')
        
        if not (fromAddress and toAddress and id_type_shipment): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        try:
            shipment = Shipment.objects.get(id = id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy Shipment"},status=status.HTTP_400_BAD_REQUEST)
        try:
            type_shipment = TypeShipment.objects.get(id=id_type_shipment)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy loại hình vận chuyển"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'id': id,
            'fromAddress': fromAddress,
            'toAddress': toAddress,
            'type_shipment': type_shipment,
        }
        serializer = ShipmentSerializer(shipment,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = Shipment.objects.all()
            serializer = ShipmentSerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
        
  

def get_use_role(username):
    headers = {'Content-Type': 'application/json'}
    url = 'http://127.0.0.1:8000/getuseraccount/'
    response = requests.get(url, params={"Username":username}, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    try:
        return data['data']['role']
    except:
        return data['error']