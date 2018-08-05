from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from users.models import UserModel, UserTicket, RecModel
from utils.functions import ticket

# 是否登录


def is_login(request):
    if request.method == 'GET':
        cookies = request.COOKIES.get('ticket')
        if cookies:
            key = UserTicket.objects.filter(ticket=cookies).first()
            data = {
                'key': key
            }
            return render(request, 'base.html', data)


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        if UserModel.objects.filter(username=username).exists() or \
                UserModel.objects.filter(email=email).exists():
            data = {
                'mgs': '该用户名或者邮箱已经被注册'
            }
            return render(request, 'register.html', data)

        if len(username) > 4 and len(username) < 21:
            if len(password) > 8 and len(password) < 21:
                UserModel.objects.create(username=username, password=make_password(password), email=email)
                return HttpResponseRedirect(reverse('user:login'))


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.filter(username=username).first()
            if check_password(password, user.password):
                respons = HttpResponseRedirect(reverse('ttsx:index'))
                rand_ticket = ticket()
                out_time = datetime.now() + timedelta(days=7)
                respons.set_cookie('ticket', rand_ticket, expires=out_time)
                UserTicket.objects.create(ticket=rand_ticket, out_time=out_time, ttsx_user_id=user.id)
                return respons
            else:
                data = {
                    'mgs': '用户名或者密码错误'
                }
                return render(request, 'login.html', data)
        return render(request, 'login.html')


# 注销
def logout(request):
    if request.method == 'GET':
        respons = HttpResponseRedirect(reverse('ttsx:index'))
        respons.delete_cookie('ticket')
        return respons


# 用户中心
def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


# 全部订单
def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


# 个人信息
def user_center_site(request):
    cookies = request.COOKIES.get('ticket')
    user_ticket = UserTicket.objects.filter(ticket=cookies).first()
    id_num = user_ticket.ttsx_user_id

    if request.method == 'GET':
        recs = RecModel.objects.filter(username_id=id_num).all()
        data = {
            'recs': recs
        }
        return render(request, 'user_center_site.html', data)

    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        address = request.POST.get('address')
        post_code = request.POST.get('post_code')
        phone = request.POST.get('phone')
        RecModel.objects.create(ruser=recipient,
                                uadress=address,
                                upc=post_code,
                                uphone=phone,
                                username_id=id_num
                                )
        recs = RecModel.objects.filter(username_id=id_num).all()
        data = {
            'recs': recs
        }
        return render(request, 'user_center_site.html', data)


