# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render

import MySQLdb
import hashlib, uuid

def home(req):
    return render(req, 'index.html', {'STATIC_URL': settings.STATIC_URL})
    #return HttpResponse("The king in the North!!!\n")

def users(req, user_id, firstname, lastname, username, email, password, birth_year, gender):
    db = MySQLdb.connect('localhost', 'root', 'al81is22te', 'loolky')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    data = None
    
    if req.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE email='%s'" % (email))
        data = cursor.fetchone()
    elif req.method == 'POST':
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        cursor.execute("INSERT INTO users (firstname, lastname, username, password, email, birth_year, gender, salt) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (firstname, lastname, username, hashed_password, email, birth_year, gender, salt));
        db.commit()
        data = {}
    elif req.method == 'PUT':
        cursor.execute("UPDATE users SET firstname='%s', lastname='%s', username='%s', email='%s', birth_year='%s', gender='%s', WHERE id=%d;" % (firstname, lastname, username, email, birth_year, gender, int(user_id)))
        db.commit()
        data = {}

    db.close()
    if data != None:
        return JsonResponse(data)

    return HttpResponse(status=500)

def login(req, email, password):
    if req.method == 'GET':
        db = MySQLdb.connect('localhost', 'root', 'al81is22te', 'loolky')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from users where email='%s' and password='%s'" % (email, password))
        data = cursor.fetchone()
        db.close()
        if data != None:
            return JsonResponse(data)

    return HttpResponse('Unauthorized', status=401)

def example(req):
    return JsonResponse({'firstname': 'Jason', 'lastname': 'DeRulo'})
