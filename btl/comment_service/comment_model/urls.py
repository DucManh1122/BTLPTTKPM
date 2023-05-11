from django.urls import path
from . import views
urlpatterns = [
    path("list/",views.comment_list),
    path("list/<int:id_pro>/",views.comment_list),
    
    path("add/",views.add_comment),
]

