from django.urls import path
from shipment_model import views 
urlpatterns = [
    path("typeshipment/",views.crud_type_shipment),
    path("shipment/",views.crud_shipment),
]