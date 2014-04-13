from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        user_id = user.id
        
        return HttpResponseRedirect('/todolist/projects'+str(user_id))
    else:
        return HttpResponseRedirect('/accounts/invalid')

def loggedIn(request):
    return render_to_response("loggedIn.html",{"full_name" : request.user.username})

def invalid_login(request):
    return render_to_response("invalid_login.html")

def logout(request):
    auth.logout(request)
    return render_to_response("logout.html")


def create_user(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("createUser.html",c)


def create_user_auth(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    confirmPassword = request.POST.get('confirmPassword','')

    if username == '' or password == '' or password != confirmPassword:
        return HttpResponseRedirect('/accounts/invalid')
    else:
        new_user = User.objects.create_user(username=username,password=password)

        user_to_login = auth.authenticate(username=username,password=password)

        if user_to_login is not None:
            auth.login(request,user_to_login)
            user_id = user_to_login.id
            return HttpResponseRedirect('/todolist/projects'+str(user_id))
        else :
            return HttpResponseRedirect('/accounts/invalid')

        
    
