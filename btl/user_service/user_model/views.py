from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user_model.serializer import AccountSerializer,UserInfoSerializer,RoleSerializer,AccountRegisterSerializer,UpdateUserInfoSerializer,LoginAccountSerializer
from .models import Role,Account,UserInfo


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def role(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response({'status':'Success','data':serializer.data},status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('role_name')
        if ( not name):
            return Response({'status':'Failed','errors': "Vui lòng nhập đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
        try:
            Role.objects.get(name = name)
            return Response({'status':'Failed','errors': "Đã tồn tại"},status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = RoleSerializer(data={'name':name})
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'Success','message':serializer.data},status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        name = request.data.get('role_name')
        id = request.data.get('id_role')
        role = Role.objects.get(id=id)
        serializer = RoleSerializer(role, data={'id':id,'name':name })
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status':'Failed','errors': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            role = Role.objects.get(id = request.data.get('id_role'))
            role.delete()
            return Response({'status':'Success','message':"Xóa thành công"},status=status.HTTP_200_OK)
        except:
            return Response({'status':'Failed','errors': "Không tìm thấy"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_login(request):
    username = request.GET.get('Username')
    password = request.GET.get('Password')
    try:
        data = Account.objects.get(username = username,password=password)
        serializer = LoginAccountSerializer(data,many=False)
        return Response({"status":"Success","message":"Welcome to Ecommerce website......",'data':serializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'status':'Failed','error': "Tên đăng nhập hoặc mật khẩu không chính xác"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    account_data ={
        'username' : request.data.get('Username'),
        'password': request.data.get('Password'),
        'confirm_password': request.data.get('Confirm Password'),
        'role': Role.objects.get(name = 'Khách hàng mới')
    }
    confirm_account_serializer = AccountRegisterSerializer(data=account_data)
    
    if confirm_account_serializer.validate(account_data):
        account_data.pop('confirm_password')
        account_serializer = AccountSerializer(data=account_data)
        if account_serializer.is_valid():
            account_serializer.create(account_data)
            return Response({'status':'Success','data':account_serializer.data},status=status.HTTP_200_OK)
        return Response({'status':'Failed','error': account_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def change_password(request):
    username = request.data.get('Username')
    new_pasword =  request.data.get('New Password')
    confirm_password = request.data.get('Confirm Password')
    password = request.data.get('Old Password')
    if not (new_pasword and confirm_password and password):
        return Response({'status':'Failed','error': "Vui lòng điền đầy đủ các trường"},status=status.HTTP_400_BAD_REQUEST)
    try:
        account = Account.objects.get(username = username)
    except:
        return Response({'status':'Failed','error': "Không tìm thấy account"},status=status.HTTP_400_BAD_REQUEST)
    account_data ={
        'id': account.id,
        'username' : account.username,
        'password': new_pasword,
        'role': account.role
    }
    try:
        Account.objects.get(username = username, password = password)
    except:
        return Response({'status':'Failed','error': "Vui lòng nhập đúng mật khẩu cũ"},status=status.HTTP_400_BAD_REQUEST)
    if new_pasword == confirm_password:
        serializer = AccountSerializer(account,data=account_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','message':'Đổi mật khẩu thành công','data':serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({'status':'Failed','error': "New password và confirm password không trùng nhau"},status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST','PUT'])
def user_info(request):
    if request.method == 'POST':
        username = request.data.get('Username')
        try:
            account = Account.objects.get(username = username)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy account"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info = UserInfo.objects.get(account = account)
            print(user_info)
            user_info_data = {
                "id" : user_info.id,
                "account": account,
                'fname' : request.data.get('First Name'),
                'lname' : request.data.get('Last Name'),
                'email' : request.data.get('Email'),
                'phone_number' : request.data.get('Phone Number'),
                'address' : request.data.get('Address'),
            }
            serializer = UpdateUserInfoSerializer(user_info,data=user_info_data)
            if serializer.is_valid():
                serializer.save()
                print("da den")
                return Response({'status':'Success','data':serializer.data},status=status.HTTP_200_OK)
        except:
            user_info_data ={
                    'fname' : request.data.get('First Name'),
                    'lname' : request.data.get('Last Name'),
                    'email' : request.data.get('Email'),
                    'phone_number' : request.data.get('Phone Number'),
                    'address' : request.data.get('Address'),
                    'account' : account
                }
            print(user_info_data)
            serializer = UserInfoSerializer(data=user_info_data)
            if serializer.validate(user_info_data):
                if serializer.is_valid():
                    serializer.create(user_info_data)
                    return Response({'status':'Success','data':serializer.data},status=status.HTTP_200_OK)
    if request.method == 'GET':
        username = request.GET.get('Username')
        try:
            account = Account.objects.get(username = username)
        except:
            return Response({'status':'Failed','error': "Không tìm thấy account"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info = UserInfo.objects.get(account = account)
            serializer = UserInfoSerializer(user_info, many=False)
            return Response({'status':'Success','data':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'status':'Failed','error': "Chưa cập nhật thông tin"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_user_account(request):
    username = request.GET.get('Username')
    try:
        data = Account.objects.get(username = username)
        return Response({"status":"Success",'data':{'username':data.username,'role':data.role.name}},status=status.HTTP_200_OK) 
    except:
        return Response({'status':'Failed','error': "Không tồn tại user"},status=status.HTTP_400_BAD_REQUEST)