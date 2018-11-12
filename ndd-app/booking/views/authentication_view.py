# -*- coding: utf-8 -*-

import json

from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


def login_page(request):
    if request.user.is_authenticated:
        return redirect('booking-page')
    return render(request, 'login.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        req = json.loads( request.body.decode('utf-8') )
        username = req['username']
        password = req['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if req['remember_me'] == True:
                request.session.set_expiry(604800)
            return JsonResponse('Success', safe=False)
        else:
            return JsonResponse('Incorrect', safe=False)

def logout(request):
    auth.logout(request)
    return redirect('login-page')
