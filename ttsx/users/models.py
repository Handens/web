
from django.db import models


# 用户模型
class UserModel(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, unique=True, null=False)

    class Meta:
        db_table = 'ttsx_user'


# 收件人信息
class RecModel(models.Model):
    username = models.ForeignKey(UserModel)
    ruser = models.CharField(max_length=20, null=False)
    uadress = models.CharField(max_length=50, null=False)
    upc = models.CharField(max_length=50)
    uphone = models.IntegerField(16, null=False)

    class Meta:
        db_table = 'ttsx_recipients'


class UserTicket(models.Model):
    ticket = models.CharField(max_length=50)
    out_time = models.DateTimeField()
    ttsx_user = models.ForeignKey(UserModel)

    class Meta:
        db_table='user_ticket'

