from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model


User = get_user_model()


######################################   API CALLS   ################################

def index(request):
    return HttpResponse('<h2>ACCOUNTS!</h2>')


def user_signup(request, username, first_name, last_name, password, email):
    if request.method == 'POST':
        print('################################### 1')
        user = get_user(username=username, email=email)
        print('################################### 2')
        if user:
            return Http404('User already exists')

        print('################################### 3')
        user = User.objects.create_user(username, email, password)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ USER: {}'.format(user))
        user.last_name = last_name
        user.first_name = first_name
        user.bla = 'bla'
        print('################################### 4')
        user.save()

        print('################################### 5')
        login(request, user)

        print('@@@@@@@@@@@@@@@@@@@@@@@@ USER: {}'.format(user))
        print('################################### 6')
        return JsonResponse(get_user_details(user), safe=False)

    return HttpResponseForbidden('allowed only via POST')


@login_required
def user_update(request):
    return HttpResponse('<h2>EXAMPLE!</h2>')


@login_required
def user_delete(request):
    return HttpResponse('<h2>EXAMPLE!</h2>')


def user_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(json.dumps(user), content_type="application/json")
    else:
        return Http404('User does not exists')


@login_required
def user_logout(request):
    logout(request)


@login_required
def password_change(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
    else:
        return Http404('User does not exists')


@login_required
def password_reset(request):
    return HttpResponse('<h2>EXAMPLE!</h2>')


##################################   PRIVATE METHODS   #############################

def get_user_details(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password,
        'email': user.email,
        'bla': user.bla
    }

def get_user(username, email):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        pass

    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        pass

    return None

