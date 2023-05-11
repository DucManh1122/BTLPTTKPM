from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category,Product,StoreHouse,Suppliers
from .serializer import CategorySerializer,ProductSerializer,StoreHouseSerializer,SuppliersSerializer
import requests
import json

# Create your views here.

@api_view(['GET','POST','PUT'])
def crud_store_house(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        address = request.data.get('Address')
        if not address: return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'address': address
        }
        serializer = StoreHouseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        address = request.data.get('Address')
        if not (address and id): return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            store_house = StoreHouse.objects.get(id=id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy nhà kho"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'id': id,
            'address': address
        }
        serializer = StoreHouseSerializer(store_house,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = StoreHouse.objects.all()
            serializer = StoreHouseSerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','POST','PUT'])
def crud_supplier(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        name = request.data.get('Name')
        phone_number = request.data.get('Phone Number')
        address = request.data.get('Address')
        if not (address and name and phone_number): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'name': name,
            'address': address,
            'phone_number': phone_number
        }
        serializer = SuppliersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    
    
    if request.method == 'PUT':
        
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        name = request.data.get('Name')
        phone_number = request.data.get('Phone Number')
        address = request.data.get('Address')
        if not (id and address and name and phone_number): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            supplier = Suppliers.objects.get(id=id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy nhà cung cấp"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'id': id,
            'name': name,
            'address': address,
            'phone_number': phone_number
        }
        serializer = SuppliersSerializer(supplier,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = Suppliers.objects.all()
            serializer = SuppliersSerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','POST','PUT'])
def crud_category(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho' and role != 'Nhân viên bán hàng':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        name = request.data.get('Name')
        if not name: return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'name': name
        }
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho' and role != 'Nhân viên bán hàng' :
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        name = request.data.get('Name')
        if not (name and id): return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(id=id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy danh mục sản phẩm"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'id': id,
            'name': name
        }
        serializer = CategorySerializer(category,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = Category.objects.all()
            serializer = CategorySerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','POST','PUT'])
def crud_product(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho' and role != 'Nhân viên bán hàng':
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)
        
        id_supplier = request.data.get('Supplier ID')
        id_category = request.data.get('Category ID')
        id_warehouse = request.data.get('Warehouse ID')
        name = request.data.get('Name')
        price = request.data.get('Price')
        image = request.data.get('Image URL')
        description = request.data.get('Description')
        amount = request.data.get('Amount')
        
        if not (name and price and image and description and amount): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        try:
            price = float(price)
            amount = int(amount)
        except:
            return Response({'status':'Failed','error': "Vui lòng nhập đúng định dạng dữ liệu"},status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=id_category)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy danh mục sản phẩm"},status=status.HTTP_400_BAD_REQUEST)
        try:
            supplier = Suppliers.objects.get(id = id_supplier)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy nhà cung cấp"},status=status.HTTP_400_BAD_REQUEST)
        try:
            storehouse = StoreHouse.objects.get(id = id_warehouse)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy kho hàng"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'name': name,
            'price': price,
            'image': image,
            'description': description,
            'amount': amount,
            'category': category,
            'supplier': supplier,
            'storehouse': storehouse
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        username = request.data.get('Username')
        role = get_use_role(username)
        if role != 'Nhân viên quản lý' and role != 'Nhân viên kho' and role != 'Nhân viên bán hàng' :
            return Response({'status':'Failed','error': "Hành động không được cho phép"},status=status.HTTP_400_BAD_REQUEST)

        id = request.data.get('id')
        id_supplier = request.data.get('Supplier ID')
        id_category = request.data.get('Category ID')
        id_warehouse = request.data.get('Warehouse ID')
        name = request.data.get('Name')
        price = request.data.get('Price')
        image = request.data.get('Image URL')
        description = request.data.get('Description')
        amount = request.data.get('Amount')
        if not (name and price and image and description and amount): 
            return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        try:
            price = float(price)
            amount = int(amount)
        except:
            return Response({'status':'Failed','error': "Vui lòng nhập đúng định dạng dữ liệu"},status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=id)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy sản phẩm"},status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(id=id_category)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy danh mục sản phẩm"},status=status.HTTP_400_BAD_REQUEST)
        try:
            supplier = Suppliers.objects.get(id = id_supplier)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy nhà cung cấp"},status=status.HTTP_400_BAD_REQUEST)
        try:
            storehouse = StoreHouse.objects.get(id = id_warehouse)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy kho hàng"},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        data = {
            'id': id,
            'name': name,
            'price': price,
            'image': image,
            'description': description,
            'amount': amount,
            'category': category,
            'supplier': supplier,
            'storehouse': storehouse
        }
        serializer = ProductSerializer(product,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success",'message':'Thay đổi thành công','data':serializer.data},status=status.HTTP_200_OK) 
        return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            data = Product.objects.all()
            serializer = ProductSerializer(data,many = True)
            return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 
        except:
            return Response({'status':'Failed','error': "Có lỗi xảy ra,vui lòng thử lại sau"},status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['GET'])      
def get_product_by_id(request):
    id = request.GET.get('Product ID')
    if not id:
        return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
    try:
        product = Product.objects.get(id=id)
    except:
        return Response({'status':'Failed','error': "Sản phẩm không tồn tại"},status=status.HTTP_400_BAD_REQUEST)
    serializer = ProductSerializer(product)
    return Response({"status":"Success",'data':serializer.data},status=status.HTTP_200_OK) 

def get_use_role(username):
    headers = {'Content-Type': 'application/json'}
    url = 'http://127.0.0.1:8000/getuseraccount/'
    response = requests.get(url, params={"Username":username}, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    try:
        return data['data']['role']
    except:
        return data['error']
