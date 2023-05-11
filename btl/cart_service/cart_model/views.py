
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart
from .serializer import CartSerializer
import requests
import json

# Create your views here.
@api_view(['GET'])
def get_cart_by_id(request):
    id = request.query_params.get('Cart ID')
    try:
        cart = Cart.objects.get(id=id)
        data = {
            "id": cart.id,
            "username": cart.username,
            "product": product_data(cart.product_id),
            "quantity": cart.quantity
        }
        return Response({"status": "success","data": data}, status=status.HTTP_200_OK)
    except:
        return Response({"status":"failed","message":"Không tìm thấy danh mục"})
@api_view(['GET'])
def cart_list(request):
    username = request.query_params.get('Username')
    carts = Cart.objects.filter(username=username)
    if carts:
        data = []
        for cart in carts:
            data.append({"id": cart.id,"username": cart.username,"product": product_data(cart.product_id),"quantity": cart.quantity})
        return Response({"status": "success","data": data}, status=status.HTTP_200_OK)
    return Response({"status":"failed","message":"Chưa có sản phẩm trong giỏ hàng"})

@api_view(['POST'])
def delete_pro_from_cart(request):
    data = {
        'id_cart' : request.data.get('Cart Id'),
    }
    try:
        obj = Cart.objects.get(id=data['id_cart'])
        obj.delete()
        return Response({"status":"success","message":"Xóa thành công"}, status=status.HTTP_200_OK)
    except:
        return Response({"status":"failed","message":"Không tìm thấy sản phẩm trong giỏ hàng"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('Product Id')
    username = request.data.get('Username')
    quantity = request.data.get('Quantity')
    pro_data = product_data(product_id)
    print(pro_data)
    
    if not(product_id and username and pro_data):
        return Response({"status":"Failed","error":"Vui lòng nhập đày đủ các trường"}, status=status.HTTP_400_BAD_REQUEST)
    # kiểm tra sản phẩm có tồn tại không
    try:
        pro_data = pro_data['error']
        return Response({"status":"Failed","error":"Sản phẩm  không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        # Kiểm tra sản phẩm đã thêm vào giỏ hàng chưa
        try:
            Cart.objects.get(username=username, product_id =product_id)
            return Response({"status":"failed","error":"Sản phẩm đã được thêm vào giỏ hàng rồi"},status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {
                'product_id' : product_id,
                'username' : username,
                'quantity' : quantity,
            }
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                serializer.create(data)
                return Response({"status":"Success","message":"product is added Successfully.","data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def product_data(productId):
    headers = {'Content-Type': 'application/json'}
    url = 'http://127.0.0.1:7999/productById/'
    response = requests.get(url, params={"Product ID":productId}, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    return data