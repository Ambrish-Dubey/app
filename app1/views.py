from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import *
import os
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required(login_url='login')
def home(req):
    
    if req.method == 'POST':
        print('*'*40)
        print('POST METHOD AT HOME')
        print('In home view:-')
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
        )
        entry.save()

        return redirect('home') #after going here, the req obj would be only accessed through get methods
    else:
        print('*'*40)
        print('GET METHOD AT HOME')
        print('In home view:-')
        print('Info:-')
        print('Request object:-',req)
        print('Get data object:-',req.GET)
        print('req.FILES:-',req.FILES)

        #showing all data to front end after getting them from POST:- 
        all = Recipe.objects.all()

        print('All the entry objects:- ',all)
        for x,y in enumerate(all):
            print('index:-',x,'Object:-',y.recipe_name,'Image name:-',y.image)

        search = req.GET.get('search')
        print(search)
        
        if search:
            search_objects = all.filter(recipe_name__icontains = search)
            print(search_objects)
            all = search_objects
        else:
            all = Recipe.objects.all()    
        dict = {'all':all}
    return render(req,'home.html',dict)

def delete(r,id):
    if r.method == 'POST':
        print('*'*100)
        print('POST METHOD AT DELETE')
        print('Data at POST:-')
        for x in r.POST:
            print(x)
        entry = Recipe.objects.get(id=id)
        print('Entry after delete:-',entry)
    else:
        print('*'*100)
        print('GET METHOD AT DELETE')
        print('Data at GET:-')
        for x in r.GET:
            print(x)
            print('r.GET:-',r.GET)

        entry = Recipe.objects.get(id=id)
        image_name = str(entry.image)
        print('Image name:- ',image_name)
        os.remove(os.path.join('Backend/',image_name))
        entry.delete()
        print('Entry Deleted')
        return redirect('home')
    
# @login_required(login_url='login')
def update(r,id):
    if r.method == 'POST':
        print('*'*100)
        print('POST at update page')
        print('Request at update page:-',r)
        print('r.POST:-',r.POST)
        print('r.FILES dictionary:-',r.FILES)

        #Data from frontend updated form:-
        recipe_name = r.POST.get('recipe_name')
        recipe_info = r.POST.get('recipe_info')
        image = r.FILES.get('image')   #gets the name only like xyz.jpeg
        print('All info just posting form:-',recipe_name,recipe_info,image)

        #Comparing imagae data from backend db:-
        object = Recipe.objects.get(id=id)
        old = object.image 

        if image == None:                               #if image file is not uplodaded on frontend form
            object.image = old
            print('Old image not deleted')
        else:
            object.image = image
            os.remove(os.path.join('Backend/',str(old)))
            print('old image deleted')

        object.recipe_name = recipe_name
        object.recipe_info = recipe_info
        
        object.save()
        print('Entry updated')

        return redirect('home')
    else:
        print('*'*100)
        print('GET at update page')
        print('Request at update page:-',r)
        print('r.POST:-',r.GET)
        print('r.FILES dictionary:-',r.FILES)

        #Trying to know which is the current id to be updated:-
        object = Recipe.objects.get(id=id) 

        print('r.method:-',r.method)

        #Information from frontend form:-
        #WE WONT RECIEVE ANY FORM OF DATA WWHEN WE REACH UPDATE FORM AS WE CAN ONLY RECIEVE DATA IF WE SUBMIT THE FORM.
        #SO PAST DATA IF UNCHANGED WONT BE DISPLAYED ON THE SHELL.
        recipe_name = r.GET.get('recipe_name')
        recipe_info = r.GET.get('recipe_info')
        image = r.FILES.get('image')   #gets the name only like xyz.jpeg
        print('All info at reaching update page:- ',recipe_name,recipe_info,image)

        print('object:-',object)

        dict = {'object':object}

        return render(r,'update.html',dict)
    

