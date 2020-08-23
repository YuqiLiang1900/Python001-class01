"""
>>> from django.contrib.auth.models import User
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('my_user', 'user@example.com', 'password')
>>> user.save()
"""


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .form import LoginForm


def index(request):
    """
    主页视图，返回 Hello 用户名
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        form = LoginForm()
        error_message = 'Please login to verify your identity.'
        context = {
            'form': form,
            'error_message': error_message,
        }
        return HttpResponseRedirect(reverse('login'), content=context)
    else:
        context = {
            'username': request.user.username,
        }
    return render(request, 'index.html', context=context)


def login_view(request):
    """
    登录视图函数
    :param request:
    :return:
    """
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index2'))
        error_message = 'Wrong username or password.'

    elif request.method == 'GET':
        form = LoginForm()

    else:
        form = LoginForm()
        error_message = 'Request method not allowed.'

    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'login.html', context)
