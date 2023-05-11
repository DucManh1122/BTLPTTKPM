from django.urls import path
from user_model import views 
urlpatterns = [
    path("register/",views.register_user),
    path("login/",views.user_login),
    path("changepassword/",views.change_password),
    path("role/",views.role),
    path("userinfo/",views.user_info),
    path("getuseraccount/",views.get_user_account)
    
]
