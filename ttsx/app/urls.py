from django.conf.urls import url

from app import views

# 主页视图
urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^user_center_order/', views.user_center_order, name='user_center_order'),
    url(r'^listre/', views.listre, name='listre'),
    url(r'^list/(?P<tid>\d+)/(?P<sid>\d+)/', views.list, name='list'),
    url(r'^detail/(?P<tid>\d+)/(?P<gid>\d+)/', views.detail, name='detail'),
    # url(r'^place_order/',views.place_order, name='place_order')
    ]