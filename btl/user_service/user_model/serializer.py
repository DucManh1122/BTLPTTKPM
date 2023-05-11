from rest_framework import serializers
from .models import Account, UserInfo, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True, many=False)
    class Meta:
        model = Account
        fields = '__all__'
        
class LoginAccountSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True, many=False)
    class Meta:
        model = Account
        exclude = ('password',)
        
        
class AccountRegisterSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True, many=False)
    confirm_password = serializers.CharField(max_length = 50)

    class Meta:
        model = Account
        fields = ('username','password','confirm_password','role')
        
    def validate(self, attrs):
        if not (attrs['username'] and attrs['password'] and attrs['confirm_password'] and attrs['role']):
            raise serializers.ValidationError({"status":"Failed","message":"Vui lòng điền đầy đủ các trường."})
        elif attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"status":"Failed","message":"Password và Confirm Password không trùng nhau."})
        else:
            try:
                Account.objects.get(username = attrs['username'])
                raise serializers.ValidationError({"status":"Failed","message":"Tên đăng nhập đã tồn tại"})
            except Account.DoesNotExist:
                return attrs
        
class UserInfoSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True, many=False)
    class Meta:
        model = UserInfo
        fields = '__all__'
        
    def validate(self, attrs):
        
        if not (attrs['fname'] and attrs['lname'] and attrs['email'] and attrs['phone_number'] and attrs['address']):
            raise serializers.ValidationError({"status":"Failed","message":"Vui lòng điền đầy đủ các trường."})
        elif not attrs['email'].endswith('@gmail.com'):
            raise serializers.ValidationError({"status":"Failed","message":"Vui lòng nhập đúng định dạng email"})
        elif len(attrs['phone_number']) != 10:
            raise serializers.ValidationError({"status":"Failed","message":"Số điện thoại yêu cầu 10 chữ số."})
        else:
            try:
                UserInfo.objects.get(email = attrs['email'])
                raise serializers.ValidationError({"status":"Failed","message":"Email đã tồn tại"})
            except UserInfo.DoesNotExist:
                return attrs

class UpdateUserInfoSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True, many=False)
    class Meta:
        model = UserInfo
        fields = '__all__'
    



