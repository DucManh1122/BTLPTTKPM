from django.urls import path
from . import views
urlpatterns = [
    path("list/",views.cart_list),
    path("list/<int:id_user>/",views.cart_list),
    
    path("add/",views.add_to_cart),
    path("get_one/",views.get_cart_by_id),
    path("delete/",views.delete_pro_from_cart)
]

