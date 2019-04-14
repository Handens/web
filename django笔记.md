django笔记   django==2.0

### 安装环境

管理环境必须先安装virtualenv

```
pip install virtualenv
```

可以快速的创建环境

还有一种方法是安装virtualenvwrapper 

```
pip install virtualenvwrapper # liunx下安装
pip install virtualenvwrapper-win # windows下安装
```

下面是virtualwrapper的部分使用方法

```
mkvirtualenv 虚拟环境名字  # 创建虚拟环境
workon 虚拟环境名字 # 进入虚拟环境名字
deactivate 退出
rmvirtualenv 虚拟环境名字 # 删除虚拟环境
lsvirtualenv # 查看所有虚拟环境
cdvirtualenv 虚拟环境名字 # 打开虚拟环境
```

### URL里面传递参数

##### 传递参数

一种是直接传参,在URL里面设置

```
urlpatterns = [
    path('book/',views.book)，
    path('book/detail/<book_id>,views.book_detail)
]
```

在views.py中接收book_id

```
def book_detail(request,book_id):
	return HttpResponse("id是%s" % book_id)
```

另外一种URL传参就是

```
urlpatterns = [
    path('book/', views.book_detail)
]
```

在路由里面就是要用?=查询数的方式，例如：

```
https://127.0.0.1/book/?id=1111
```

在views.py 中不用接收book_id

```
def book_detail(request):
	id = request.GET.get('id')
	return HttpResponse('id是%s' % id)
```

##### 传递参数转换，指定类型

必须符合类型才能通过访问，否则不能访问

如果不写的话，默认为str的转换器，只要不出现"/"字符都可以正常访问

指定int 类型 （只能使用阿拉伯数字）

```
urlpatterns = [
    path('book/',views.book)，
    path('book/detail/<int:book_id>,views.book_detail)
]
```

指定slug类型(阿拉伯，字母，_)都可以

```
urlpatterns = [
    path('book/',views.book)，
    path('book/detail/<slug:book_id>,views.book_detail)
]
```

指定path类型 （所有都可以)

```
urlpatterns = [
    path('book/',views.book)，
    path('book/detail/<path:book_id>,views.book_detail)
]
```

自定义URL转换器

在子url里面

例如 :python+django+flask

```
urlpatterns = [
    path('', views.article),
    path("list/<cate:categories>", views.article_list)
]
```

定义类

```
class  categoryConverter(object):
	regex = r'\w+|((\w+\+\w+)+)'
	
	def to_python(self, value):
		result = value.splite("+")
		return result
		
	def to_url(self,value):
		if isinstance(value, list)
			teturn result
		else:
			raise RuntimeError("转换URL的时候，分类参数必须为列表！")
	register_converter(categoryConverter,"cate")
		
```



##### URL分层

包含其他app中的URL

应该使用include函数包含子URL

```
urlpatterns = [
    path('book/', include('app.urls'))
]
```

在子URL里面使用URL(空字符默认的是book首页)

```
urlpatterns = [
    path('', views.book_detail)
]
```

在子URL里面可以使用命名

```
urlpatterns = [
    path('/signin', views.login, name='login')
]
```

在跳转的时候就必须反转

这里是login而不是signin了

```
from django.url import reverse，redirect
def login(request):
	return redirect(reverse('login'))
```

如果不加name的话

```
from django.url import reverse, redirect
def login(request):
	return redirect('signin')
```

##### 应用命名空间

如果，多个app中为了防止多个同名，为了反转的时候不出错误运用命名空间

只要在app中的url.py中添加app_name变量

 ```
app_name = "book"

urlpatterns = [
    path('/signin', views.login, name='login')
]
 ```

那么反转的时候就要加参数

```
from django.url import reverse，redirect
def login(request):
	return redirect(reverse('book:login'))
```

##### 实命名空间、

多个url映射到同一个url中，使用实例命名空间，在主url中include中添加namespace

```
urlpatterns = [
    path('cms1',include(cms.urls, namespace='cms1')),
    path('cms2',include(cms.urls, namespace='cms2'))
]
```

在做反转的时候,使用   request.resolver_match.namespace  获取到当前的命名空间

```
def index(request):
	current_namespace = request.resolver_match.namespace
	return redirect(reverse("%s:login" % current_namespace))
```

##### include的使用

如果在主页面中使用 

```
urlpatterns = [
    path('book/', include('book.urls), namespace="book")
]
```

那么就必须在子urls.py中添加app_name = "book"

如果不在子urls.py中添加就可以写成这样

```
urlpatterns = [
    path('book/', include(('book.urls,'book'), namespace="book")
]
```

##### reverse

如果再反转的时候想要添加参数，那么可以传递"kwargs"添加到reverse当中。

```
detail_url = reverse('detail', kwargs={"page":1,"id":111})
```

如果想要添加查询字符串的参数，那就必须手动添加拼接

```
login_url = reverse('login') + "?next=/"
```

### 常用基本标签

使用template渲染的时候。不想{{}}或者{% %}时候用

```
{% verbatim %}
{% endverbatim %}
```

使用 template 渲染的时候，用URL传参

```
<a herf="{% url '页面.html' name='1' %}">
```

如果有 查询参数

```
<a herf={% url '页面.html' %}?next=/>
```

使用add 拼接

```
{{ value|add:"value2" }}
```

使用cut删除

```
{{ value|cut:""}}
```

使用data日期格式化

```
{{ today:date:"y/m/d"}}
```

默认值(没有参数的时候)

```
{{ value|dafalut:"默认值"}}
```

使用第一个或者最后一个

```
{{ value|first}}
{{ value|last }}
```

控制小数点(不写后缀数字默认保留一位小数，四舍五入，)

```
{{ value|format3}}
```

使用长度

```
{{ value|length}}
```

切片

第一个数开始，第二个数终止 第三个 步长

```
{{ value|slice:"0:2:2" }}
```

删除html所有标签

```
{{ value:striptags}}
```

指定显示几个开始几个值

```
{{ value:truncatechars:"5"}}
```

自定义过滤器 创建文件夹必须名字叫 templatetags

```
from django import template
register = template.Library()

def greet(value, word):
	return value + word

register.filter("greet", greet")
```

或者使用

```
from django import template
register = template.Library()

@register.filter	 
def greet(value, word):
	return value + word
```

公共代码  把公共代码放在一个html当中

不同的地方

```
{% block content%}
{% enblock %}
```

继承模板

```
{% extends "base.html" %}
在不同的地方
{% block content %}
{% endblock %}
```

如果要继承公共模板里面的内容

```
{% block.super %}
```



### 数据库

数据库表命名

```
class Mata:
	db_table = "book"
```

外键

删除model1中的数据时候，model也会删除

```
model = model.CharFiles("model1",on_delete = model.CASCADE)
```

一对一

```
user = models.OneToOneField("model1", ondeleta = model.CASCADE)
```

多对一

```
user =models.ForeyKey(models, on_delete = model.CASCADE)
```

已经有的数据库生成对应的模型(重定向到model.py文件中)

```
python manage.py inspectdb > models.py

```

数据库中添加索引



创建表的时间直接添加索引

​	创建普通索引

```
CREATE TABLE book
(
	book_id int NOT NULL,
	username VARCHAR(16) NOT NULL,
	INDEX(username)
);
```

​	创建唯一索引

```
CREATE TABLE t1
(
	id INT NOT NULL,
	name CHAR(30) NOT NULL,
	UNIQUE INDEX UniqIdx(id)
);
```

​	创建主键索引

```
CREATE TABLE t2
(
	Id INT NOT NULL，
	name CHAR(10),
	PRIMARY KEY(Id)
);
```

​	创建组合查询

```
CREATE TABLE t3
(
	id INT NOT NULL,
	name CHAR(10) NOT NULL,
	age INT NOT NULL,
	info VARCHAR(255),
	INDEX MultiIdx(id,name,info)
);
```

在已经创建的表上，创建

```
CREATE INDEX 索引名字 ON 表(字段)
```

查看索引

```
SHOW INDEX FROM 表/G
```

删除索引

```
DROP INDEX 索引名 ON 表
```





### 查询

查询

```  
model.Objects.filter(id__exact=1)   等于“=”
model.objects.filter(name__iexact = "%look")   等会LIKE
model.Objects.fliter(name__contains="hello")   区分大小写 包含
model.Objects.filter(title__icontains="hello")   不区分大小写 包含
model.Objects.filter(id__in[1,2,3])    查询 id为1 2 3 
model.Objects.filter(title__iragex=r'^abc')  查询正则表达式  区分大小写 
```

聚合函数

annotate 分组  aggregate不分组

```
from django.db.models import Avg，count
Book.objects.aggregate(avg = Avg("pritice))  平均数

Book.object.annotate(avg = Avg("pritice))  平均数（分组）

Book.object.aggregate(num = count("id"))  统计个数
Book.object.aggregate(num = count("name",distinct=True))  统计个数(去掉重复)

Book.object.aggregate(Max（'age'),Mix("age")) 最大值，最小值

Book.object.aggregate(sum("price")) 总共
```

F表达式

```
from django.db.models import F

s.objects.updata(b=F("b"+1000))  不用提出在数据库中运行  在s表中的b字段全部加上1000
b.objects.filter(name=F("price"))  名称和price相等
```

Q函数

```
from django.db.models import Q
s.objects.filter(Q(a__lt=10) | Q(b__lt=20)) 或者
s.objects.filter(Q(a__lt=10) & Q(b__lt=20)) 并且
```

### queryset API

```
filter 是满足条件的
s.object.filter(name="abc")  可以跟 s.object.filter(name="abc").filter(old=19)

exclude 不满足条件
s.object.exclude(name="abc")

annotate 每条查询语句
s.objects.annotate(b__price=F("b__price"))  可以使用每条属性但是price用b__price

oder_by排序

value 只提取单个数字
s.objects.value("id", "name")  返回的值是字典
defer和value用法一样，返回值是对象 
defer是过滤掉
only只会查到需要的值，返回的也是queryset对象
value_list 返回值是元祖
s.objects.value_list("id", flat=Ture) 返回的是值，但是只能用在一个字段中 

select_related  查找相关表的数据
s.objects.select_related("name")  name为外键  这种只能用在一对一，一对多

s.objects.prefetch_related("name")  多对多，或者是多对一
如果查找出来的结果还要筛选
perfetch = prefetch("book_set",queryset=b.objects.filter(price__gte=90))
bs b.object.prefetch_ralated(prefetch)
for b in bs:
	bss = b.book_set.all()
	for bsss in bs:
		print("bsss")


```

添加数据

```
b.objects.create(name=1)   添加一条数据
b.objects.bulk_create([a(name="123"), c(name="456")]) 添加多条
```

统计个数

```
b.objects.count()
```

去掉重复数据

```
b.object.filter(c__gte=80).distinct()
```

### django限制请求method

获取ip地址

```
if request.META.has_key("HTTP_X_FORWARDED_FOR"):
	ip= request.META['HTTP_X_FORWARDED_FOR']
else:
	ip = request.META["REMOTE_ADDS"]
```

文件列表

用listview  参数如下

```
class view(ListView):
	model = aaa   # 模型名字
	template_name = "aa.html"  # 模板
	context_object_name = "article"  # 模板名字
	paginate = 10 # 分页
	ordering = "id" # 分页顺序
	page_kwarg = "p" # 分页参数
	
	def get_queryset(self):
		return b.objects.all()  获取限制调制
```



### 表单

表单验证，使用Form 

还可以使用fileForm



### 上传文件

在配置里面最下面添加

```
MEDIA_ROOT = os.path.join(BASE_DIR, '文件名')
MEDIA_URL = "/文件名/'
```

然后再url.py里面

```
urlpatterns = [
    path('', views.index),
]+static(setting.MEDIA_URL,document_root=setting.MEDIA_ROOT)
```

同时制定model

```
class upload(models.Model):
	upload = models.FileField(upload_to = "%Y/%m/%d")
```



### mencached

分布式缓存    储存验证码，登陆session不关键的数据



### cookie

设置cookie

```
def index(request):
	response = HttpResponse("index")
	response.set_cookies('username','1111',max_age=180)
```

获取cookie

```
cookie = request.COOKIES
username = cookies.get('username')
```

删除cookie

```
 response = HttpResponse('delete')
 response.delete_cookie('username')
```



### session

设置session

```
request.session['username'] = '111'
```

获取session值

```
request.session.get('username')
```

获取并且删除

```
request.session.pop('username')
```



删除数据

```
request.session.flush() 删除所有数据
```

设置有效时间

```
request.session.set_expiry(0)  0:浏览器退出时效，None：默认两周
```

删除过期时间  不会自动删除，需要手动删除

```
request.session.clear_expiry() 
```

一般采用缓存加数据库的方式存储session

首先现在setting里面添加

```
CACHES = {
    'default': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
}

SESSION_ENGINE = 'django.contrib.session.backends.cached_db'

```



### 上下文管理器

 多个页面重复的状态

比如登陆

常用的上下文管理器 debug, request, auth,messages,media,static,csrf



中间件

使用函数的中间件

```	
def simple_middleware(get_response):
	def middleware(request)
		条件写在这里
		response = get_response(request)
		return response
	return middleware
```



使用类的中间件

```
class imple_middleware(object):
	def __init__(self, get_response):
		self.get_response = get_response
		
	def __call__(self, request):
		条件
		response = self.getresponse(request)
		return response
```

内置中间件

commonMiddleware :不加“/“的时候，自动给加上  必须有“user-Agent'

GZipMiddleware  返回的数据进行压缩

MessageMiddleware  处理消息中间件

securityMiddleware 消息安全的中间件 防止xss防御请求头， 可以http转换成https

sessionMiddleware 处理session对象

Authenticationmiddleware  会给reuqest 添加一个user对象的中间件

CsrfViewMiddleware 保护crsf的中间件

XFrameOptionsMiddleware   不允许，别的网站加载



### CSRF (跨站域身份伪造)

访问病毒网站的时候模拟用户像相关网站发送信息 



### xss跨文本攻击

不需要富文本用escape

 需要富文本

```
import bleach
from bleach.sanitizer import ALLOWED_TAGS,ALLOWED_ATTRIBUTES 
tags =ALLOWED_TAGS + ['img']   # 默认不够时候，添加
ALLOWED_ATTRIBUTES = {**ALLOWED_ATTRIBUTES，'img':['src']}
bleach.clean(获取的参数,tags=ALLOWED_TAGS，attributes=ALLOWED_ATTRIBUTES)
```

### clickjacking

前端利用ifream，不是点击自己的而是其他的网页

解决问题在中间件中添加

```
django.middleware.clickjacking.XFrameOpitionsMiddleware
```

### SQL注入

在web中使用SQL语句，实行查询语句

不能使用直接拼接的形式 使用参数

不能使用管理员的权限链接数据库

不能把机密的信息直接存放，加密或者hash去掉密码的敏感的信息
应用出现异常的时候，尽可能少些一点提示，最好使用自定义的错误信息对原始错误信息进行包装

### Redis

1，登陆回话储存

2， 排行榜/计数器

3，作为消息队列 比如celery

4，当前在线人数

5，常用数据缓存 

6，把前多少文章、评论存在缓存中

7，好友关系

8，发布和订阅



安装

```
sudo apt-get install redis-server
```

卸载

```
sudo apt-get purge --auto-remove redis-server
```

启动

```
sudo service redis-server start
```

查看命令

```
ps aux|grep redis
```

停止

```
sudo service redis-server stop
```

连接

```
redis-cli -h 地址 -p 端口
```

添加

```
set key value 如： set username xiaotuo
```

删除

```
del key 
```

设置过期时间

```
expire key timeout(单位为秒)
```

​		也可以

```
set key value EX timeout
或
setex key timeout value
```

查看过期时间

```
ttl key 
如 ttl username
```

查看当前所有key

```
keys *
```

列表操作

```
lpush key value  从左边添加
rpush key value  从右边添加
lrange key start stop  查看  例如查看全部 lrange key 0 -1
lpop key 左边移出并且返回列表
rpop key 移出并且返回列表
lindex key index 返回第几个元素
llen key 获取列表中元素个数
lrem key count value  删除指定的元素 count指定的为0的删除全部 count>0删除前面几个 反之
```

集合操作

```
sadd set value1 value2... 添加元素
smembers set 查看元素
srem set member... 移出元素
scard set 查看元素个数
sinter set1 set2 获取多个集合的交集
sunion set1 set2 获取多个集合的并集
sdiff set1 set2 获取多个集合的差集
```

哈希操作

```
hset key fiekd value 添加
hget key filld 查看
hdel key field 删除
hgetall key 查看当前某个哈希中所有的键和值 
hkeys key 获取哈希中所有的键
hvals key 查看哈希中所有的值
hlen key 总共的所有键值对个数
```

事物操作

```
可以隔离操作：按顺序序列化执行
原子操作：要不全部执行，要不全部不执行
multi 以后执行的所有命令都在事物中执行
exec 执行事物，和multi一并提交
discard 取消所有事物
watch 监视事物
unwatch 取消监视
```

发布和订阅

```
subscribe 某个频道  # 可以多个频道
publish 某个频道 message
```

 

有两种同步机制

RDB和AOF



redis指定密码

在redis.conf

```
requirespass  password # password为密码
auth password 登录 
```

别的电脑想链接

在配置文件中添加本地的IP地址原来的127.0.0.1可以不删除

```
bind IP 
```

Python操作redis

首先

```
pip install redis
```

新建一个文件

```
from redis import Redis
cache = Redis(host='ip',port=6379,password='zhidao')
```

对字符串操作

```
cache.set('username', ' abcx') 设置一个值
```



### django环境搭建





