from home.views import *
from django.urls import path,include

urlpatterns = [
    
    # path('',index_page,name='index_page'),
    path('login/',login_page,name='login'),
    path('',register,name='register'),
    path('logout/',logout_user,name='logout'),
    path('personal/<str:username>',personal,name='personal'),
    path('delete_personal/<id>/<username>',delete_personal,name='delete_personal'),
    path('update_personal/<id>/<username>',update_personal,name='update_personal'),


    
    
]