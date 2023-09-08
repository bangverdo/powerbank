from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Bak
import logging
import logging.handlers


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')



def start_log(request):
    filehandler = logging.FileHandler(f'./logs/logfile_{request}.log', encoding='utf-8')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    return filehandler

def stop_log(filehandler):
    logger.removeHandler(filehandler)

def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect("main:login")
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "main/change_pw.html",context)

def remit(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("password")
        user = request.user
        puser = request.POST.get("pname")
        if int(request.POST.get("bak")) > 0:
            if check_password(current_password,user.password):
                for pname in User.objects.values('username'):
                    if "%s"%pname in "{'username': '%s'}"%puser:
                        gmoney = Bak.objects.get(user=user)
                        
                        pid = str(User.objects.filter(username=puser).values('id'))[18:20]
                        if "}" in pid:
                            pid = pid[0:1]
                        pmoney = Bak.objects.get(user=int(pid))

                        if gmoney.money < int(request.POST.get("bak")):
                            context.update({'error':"잔고가 부족합니다."})
                        else:
                            if str(User.get_username(user)) == str(puser):
                                context.update({'error':"본인에게 송금은 불가합니다."})
                            else:
                                gmoney.money = gmoney.money - int(request.POST.get("bak"))
                                pmoney.money = pmoney.money + int(request.POST.get("bak"))
                                gmoney.save()
                                pmoney.save()
                                a = start_log('goverment')
                                b = start_log(puser)
                                c = start_log(User.get_username(user))
                                logger.info(User.get_username(user)+ " 송금 " +  request.POST.get("bak") + "박 " + puser)
                                context.update({'error':"정상적으로 처리되었습니다."})
                                stop_log(a)
                                stop_log(b)
                                stop_log(c)
                        return render(request, "main/remit.html",context)
                    
                context.update({'error':"받는 사람 이름을 다시 확인해주세요."})
            else:
                context.update({'error':"비밀번호가 일치하지 않습니다."})
        else:
            context.update({'error':"금액은 자연수로 입력해주세요"})

    return render(request, "main/remit.html",context)

def balance(request):
    context= {}
    
    user = request.user

    testFile = open(f'./logs/logfile_{User.get_username(user)}.log','rt')

    gmoney = Bak.objects.get(user=user)


    logs = testFile.readlines()
    context.update({'logs':logs})
    context.update({'balance':gmoney.money})
    testFile.close()
                        
    return render(request, "main/balance.html",context)

def log(request):
    context= {}

    testFile = open('./logs/logfile_goverment.log','rt')

    logs = testFile.readlines()
    context.update({'logs':logs})

    testFile.close()
                        
    return render(request, "main/log.html",context)

def gmoney(request):
    context= {}
    if request.method == "POST":
        puser = request.POST.get("pname")
        if int(request.POST.get("bak")) > 0:
            
            for pname in User.objects.values('username'):
                if "%s"%pname in "{'username': '%s'}"%puser:
                    
                    
                    pid = str(User.objects.filter(username=puser).values('id'))[18:20]
                    if "}" in pid:
                            pid = pid[0:1]
                    pmoney = Bak.objects.get(user=int(pid))
                    a = start_log('goverment')
                    b = start_log(puser)
                    if str(request.POST.get("gtype")) == "sang":
                        pmoney.money = pmoney.money + int(request.POST.get("bak"))
                        logger.info("정부 상금 " +  request.POST.get("bak") + "박 " + puser + " 사유: " + str(request.POST.get("why")))
                    else:
                        pmoney.money = pmoney.money - int(request.POST.get("bak"))
                        logger.info("정부 벌금 " +  request.POST.get("bak") + "박 " + puser + " 사유: " + str(request.POST.get("why")))
                    stop_log(a)
                    stop_log(b)
                    pmoney.save()
                    
                    context.update({'error':"정상적으로 처리되었습니다."})
                    return render(request, "main/gmoney.html",context)
                
            context.update({'error':"받는 사람 이름을 다시 확인해주세요."})
        else:
            context.update({'error':"금액은 자연수로 입력해주세요"})

    return render(request, "main/gmoney.html",context)


# Create your views here.
