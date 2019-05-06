# -*- coding: utf-8 -*-

import json

from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect, render


def login(request):
    template_name = 'login.html'

    if request.user.is_authenticated:
        return redirect('dashboard-page')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            if request.POST['remember_me'] == '1':
                request.session.set_expiry(604800)
            return redirect('dashboard-page')
        else:
            messages.error(request, 'Incorrect Username or Password')

    return render(request, template_name)

def logout(request):
    auth.logout(request)
    return redirect('login')
