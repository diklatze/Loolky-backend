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
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils import timezone


User = get_user_model()
CHARACTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*'
FROM_EMAIL_ADDRESS = 'loolky2015@gmail.com'
RESET_EMAIL_SUBJECT = 'Loolky reset password notification'
RESET_EMAIL_BODY = 'Hello {} {},\n\nYour new temporary password is: {}\n\nThe temporary password will be valid for 1 hour.\n\nThank You,\nLoolky team'


######################################   API CALLS   ################################

#@csrf_exempt
def index(request):
    return HttpResponse('<h2>ACCOUNTS!</h2>')


#@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        user = get_user(username=user_info['username'])
        if user:
            return Http404('User already exists')

        user = User.objects.create_user(user_info['username'], user_info['email'], user_info['password'])
        set_user_additional_details(user, user_info)
        user.save()

        return JsonResponse(user, safe=False)

    return HttpResponseForbidden('allowed only via POST')


def user_signup_done(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        user = authenticate(request, username=user_info['username'], password=user_info['password'])
        if not user:
            return Http404('wrong details')

        if user and user.is_valid_account:
            return Http404('User already confirmed')

        user.is_valid_account = True
        user.save()
        return HttpResponse('User signup process confirmed')

    return HttpResponseForbidden('allowed only via POST')


#TODO: maybe to check if too many attemps of wrong login attempts were made
def user_login(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        username = user_info.get('username', None)
        email = user_info.get('email', None)
        password = user_info.get('password', None)
        temporary_password = user_info.get('temporary_password', None)

        user = get_user(username=username, email=email)
        if not user:
            return Http404('User does not exists')

        # authenticate and login (try with regular password and if fails try with temporary password)
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            login(request, authenticated_user)
            return JsonResponse(get_user_details(authenticated_user), safe=False)

        # login failed, but maybe the user is using a reseted password
        time_delta = timezone.now() - user.temporary_password_date
        if user.temporary_password_date and time_delta < datetime.timedelta(hours=1) and \
            temporary_password == user.temporary_password:
            user.temporary_password = None
            user.temporary_password_date = None
            user.set_password(temporary_password)
            user.save()

            login(request, user)

            return JsonResponse(get_user_details(user), safe=False)

        return Http404('Incorrect username or password')

    return HttpResponseForbidden('allowed only via POST')


@login_required
def user_logout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Http404('not authenticated')
        logout(request)
        return HttpResponse('Logged out successfully')

    return HttpResponseForbidden('allowed only via POST')


@login_required
def change_password(request):
    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Http404('not authenticated')

        user_info = json.loads(request.body)
        request.user.set_password(user_info['new_password'])
        request.user.save()

        # need to login after changing password from django 1.7
        login(request, request.user)

        return HttpResponse('Password changed successfully!')

        # #TODO: not sure the authenticate here is needed because we have the login_required decorator
        # user = authenticate(request, username=username, password=current_password)
        # if user is not None:
        #     user = User.objects.get(username=username)
        #     user.set_password(new_password)
        #     user.save()
        #     return HttpResponse('Password changed successfully!')
        # else:
        #     return Http404('User does not exists')

    return HttpResponseForbidden('allowed only via PUT')


#TODO: change the reset mechanism so it will send and email to the user, then he will press on a
#      link where he can change his password
def reset_password(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        username = user_info.get('username', None)
        email = user_info.get('email', None)

        user = get_user(username=username, email=email)
        if not user:
            return Http404('User does not exists')

        user.temporary_password = generate_password()
        user.temporary_password_date = timezone.now()
        user.save()

        body = RESET_EMAIL_BODY.format(user.first_name, user.last_name, user.temporary_password)
        send_email(user.email, RESET_EMAIL_SUBJECT, body)

        return HttpResponse('An email was sent with a new temporary password')

    return HttpResponseForbidden('allowed only via POST')


@login_required
def user_update(request):
    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Http404('not authenticated')

        user_info = json.loads(request.body)
        set_user_additional_details(request.user, user_info)
        request.user.save()
        return HttpResponse('User update succeeded')

    return HttpResponseForbidden('allowed only via PUT')


##################################   PRIVATE METHODS   #############################

def get_user_details(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password,
        'email': user.email,
        'height': user.height,
        'gender': user.gender,
        'country': user.country,
        'city': user.city,
        'shirt_size': user.shirt_size,
        'pents_size': user.pents_size,
        'bra_size': user.bra_size,
        'shoe_size': user.shoe_size,
        'picture': user.picture,
        'is_valid_account': user.is_valid_account
    }


def get_user(username=None, email=None):
    if username:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            pass

    if email:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            pass

    return None


def generate_password():
    temporary_password = ''

    for i in range(0, 15):
        temporary_password += random.choice(CHARACTERS)

    return temporary_password


def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_EMAIL_ADDRESS, 'Aa#@!456')
    text = msg.as_string()
    server.sendmail(FROM_EMAIL_ADDRESS, to_address, text)
    server.quit()


def set_user_additional_details(user, user_info):
    user.last_name = user_info['last_name']
    user.first_name = user_info['first_name']
    user.height = user_info['height']
    user.gender = user_info['gender']
    user.city = user_info['city']
    user.country = user_info['country']
    user.shirt_size = user_info.get('shirt_size', 0)
    user.pents_size = user_info.get('pents_size', 0)
    user.bra_size = user_info.get('bra_size', '0')
    user.shoe_size = user_info.get('shoe_size', 0)
    user.picture = user_info.get('picture', 'pic1')
