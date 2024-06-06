from django.urls import path
from app1.views import *

urlpatterns = [
    path('',home,name='home'),
    path('delete/<id>',delete,name='delete'),
    path('update/<id>',update,name='update'),


]
