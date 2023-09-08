from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Bak
import logging
import logging.handlers

for pname in User.objects.values('id'):
    pid = str(pname)[18:20]
    print(pid)

    #pmoney = Bak.objects.create(user=int(pid), )