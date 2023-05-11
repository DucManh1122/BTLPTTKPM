from django.urls import path
from product_model import views 
urlpatterns = [
    path("storehouse/",views.crud_store_house),
    path("supplier/",views.crud_supplier),
    path("category/",views.crud_category),
    path("product/",views.crud_product),
    path("productById/",views.get_product_by_id),
]