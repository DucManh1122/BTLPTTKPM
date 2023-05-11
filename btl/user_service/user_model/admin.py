from django.contrib import admin
from user_model.models import Account,Role,UserInfo
# Register your models here.

admin.site.register(Account)
admin.site.register(Role)
admin.site.register(UserInfo)
