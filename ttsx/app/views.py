from django.http import HttpResponseRedirect
from django.shortcuts import render


from django.urls import reverse

from app.models import TypeInfo, GoodsInfo, CartInfo

# 主页
from users.models import UserModel, UserTicket


def index(request):
    if request.method == 'GET':
        types = TypeInfo.objects.all()
        goods = GoodsInfo.objects.all()
        data = {
            'types': types,
            'goods': goods
        }
        return render(request, 'index.html', data)


# 购物车
def cart(request):
    if request.method == 'GET':
        return render(request, 'cart.html')


# 全部订单
def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


# 跳转到列表
def listre(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('ttsx:list', kwargs={'tid': 0, 'sid': 0}))


# 商品列表
def list(request, tid, sid):
    if request.method == 'GET':
        types = TypeInfo.objects.all()
        if tid=='0':
            goods = GoodsInfo.objects.all()
        else:
            goods = GoodsInfo.objects.filter(gtype_id=tid)
        if sid=='0':
            pass
        if sid=='1':
            goods=goods.order_by('gprice')
        if sid=='2':
            goods=goods.order_by('-gprice')
        return render(request, 'list.html', {'types': types, 'goods': goods, 'tid': int(tid), 'sid': sid})


# 商品详情
def detail(request, tid, gid):
    if request.method == 'GET':
        good = GoodsInfo.objects.filter(gtype_id=tid, id=gid).first()
        data = {
            'good': good
        }
        return render(request, 'detail.html', data)


# 添加购物车
def add_goods(request, gid):
    if request.method == 'POST':
        cookies = request.COOKIES.get('ticket')
        user_ticket = UserTicket.objects.filter(ticket=cookies).first()
        id_num = user_ticket.ttsx_user_id
        count = 1
        if CartInfo.objects.filter(good_id=gid):
            count += 1
        CartInfo.objects.create(count=count,
                                user_id=id_num,
                                goods_id=gid,
                                good_statu=1
                                )


# 删除商品
def del_goods(request, gid):
    count = 1
    if CartInfo.objects.filter(good_id=gid):
        count -= 1
    else:
        CartInfo.objects.filter(goods_id=gid).delete()