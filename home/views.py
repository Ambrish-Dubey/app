from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from app1.models import *
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages
import time
from django.contrib.auth import authenticate,login,logout
import os
from django.contrib.auth.decorators import login_required

def index_page(request):
    return render(request,'Register.html')

def login_page(request):
    if request.method == 'POST':
        print('*'*100)
        print('Request at post of login page')
        print('Request:-',request)
        print('Request method:-',request.method)

        #Data from form frontend:-
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Data fetching from db for verification:-
        user = User.objects.filter(username = username, password = password) 
        print(user)

        if user:
            print('Successful Username')
            
            # messages.success(request,'Successfull login')

            #Save the session of the user who has logged in.
            login(request,user[0])

            username = str(user[0].username)

            return redirect('personal',username)
        else:
            print('Invalid Username or Password entered')
            messages.error(request,'Invalid Username or Password')
            return redirect('login')
    else:
        print('*'*100)
        print('Request at get of login page')
        print('Request:-',request)
        print('Request method:-',request.method)
        return render(request,'Login.html')

def register(request):
    if request.method == 'POST':
        print('*'*100)
        print('Request at post of login page')
        print('Request:-',request)
        print('Request method:-',request.method)

        #Data from frontend form:-
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Verifying if the username is already taken:-

        #Fetching objects on the basis of username:-
        same_username = User.objects.filter(username = username)
        print('same_username:-',same_username)

        if same_username.exists():                                  #or len(same_username) != 0
            print('Username already taken')
            messages.warning(request,'Username already taken, Try another!')
            return redirect('register')
        else:
            #Object creation at Backend:- 
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                password = password)
            
            # messages.success(request,'Account created successfully')
            
        #Just to encrypt pasword:-
        # user.set_password(password)     #password = password but encrypted also

        user.save()

        username = user.username

        return redirect('personal',username)
    else:
        print('*'*100)
        print('Just at Register entry page with GET method')
        print('request:-',request)
        print('request.method:-',request.method)
        return render(request,'Register.html')

def lodaing(request):
    return render(request,'loading.html')

def logout_user(request):
    logout(request)     #Deletes the session of the current user
    return redirect('login')

@login_required(login_url='login')
def personal(req,username):
    if req.method == 'POST':
        print('*'*100)
        print('POST METHOD AT PERSONAL')
        print('In personal view:-')
        print('Info:-')
        print('Request object:-',req)
        print('Post data object:-',req.POST)
        print('req.FILES:-',req.FILES)

        #getting data after user submits the button with post method:-
        recipe_name = req.POST.get('recipe_name')
        recipe_info = req.POST.get('recipe_info')
        image = req.FILES.get('image')   #gets the name only like xyz.jpeg
        print(recipe_name,recipe_info,image)

        #sending to backend:-
        entry = Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_info = recipe_info,
            image = image,
            user=req.user
        )
        entry.save()

        return redirect('personal',username) #after going here, the req obj would be only accessed through get methods
    else:
        print('*'*40)
        print('GET METHOD AT PERSSONAL')
        print('In personal view:-')
        print('Info:-')
        print('Request object:-',req)
        print('Get data object:-',req.GET)
        print('req.FILES:-',req.FILES)

        # username = req.GET.get('user')
        print('username:-',username)

        all = User.objects.all()
        print('all:-',all)

        
        # for objects in all:
        #     if username in objects.username:
        #         print('Username collectd and user entered!')
        #         logged_in_user = User.objects.get(username=username)
        #         print('Object found')
        
        logged_in_user = req.GET.get('user')
        print('logged_in_user:-',logged_in_user)


        # recipe_all = Recipe.objects.all(user = logged_in_user)
        recipe_all = Recipe.objects.filter(user = logged_in_user)
        print('recipe_all:-',recipe_all)

        search = req.GET.get('search')
        print(search)
        
        if search:
            search_objects = recipe_all.filter(recipe_name__icontains = search)
            print(search_objects)
            all = search_objects
        else:
            # all = Recipe.objects.all(user = logged_in_user)    
            all = Recipe.objects.filter(user = logged_in_user)    

        dict = {'all':all,'user':username}

    return render(req,'personal.html',dict)

def delete_personal(req,id,username):
    print('*'*100)
    print(f'req {req} at req.method:- {req.method} of DDelete page')
    object = Recipe.objects.get(id=id)
    print('object:-',object)
    image_name = str(object.image)
    print('Image to be deleted:-',image_name)
    os.remove(os.path.join('Backend/',image_name))
    print('image deleted')
    object.delete()
    print('Recipe removed')
    return redirect('personal',username)

def update_personal(req,id):
    pass