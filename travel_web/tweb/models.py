from django.db import models


# Create your models here.
class City(models.Model):
    Cid = models.AutoField(primary_key=True)
    Cname = models.CharField(max_length=10, unique=True, null=False)
    Cum_X = models.IntegerField(null=False)

    class Meta:
        db_table = 'city'


class Snack(models.Model):
    Sid = models.AutoField(primary_key=True)
    S_name = models.CharField(max_length=255, null=True)
    S_city = models.ForeignKey('City', to_field='Cname', on_delete=models.RESTRICT, db_column='S_city', null=True)
    S_pic_url = models.CharField(max_length=255, null=True)
    S_Introduce = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = 'snack'


class ScenicZone(models.Model):
    SZid = models.AutoField(primary_key=True)
    SZ_name = models.CharField(max_length=50, null=True)
    SZ_city = models.ForeignKey(City, to_field='Cname', on_delete=models.RESTRICT, db_column='SZ_city', null=True)
    SZ_message = models.IntegerField(null=True)
    SZ_score = models.FloatField(null=True)
    SZ_popularity = models.IntegerField(null=True)
    SZ_address = models.TextField(null=True)
    SZ_time = models.CharField(max_length=100, null=True)
    SZ_introduce = models.TextField(null=True)
    SZ_pic_url = models.CharField(max_length=255, null=True)
    SZ_sIntroduce = models.TextField(null=True)

    class Meta:
        db_table = 'scenic_zone'


class User(models.Model):
    UID = models.AutoField(primary_key=True)
    Uname = models.CharField(max_length=20, null=False)
    Uemail = models.CharField(max_length=255, null=False)
    Upwd = models.CharField(max_length=16, null=False)
    jurisdiction = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'user'


class UserCheck(models.Model):
    email = models.CharField(max_length=255, null=True)
    check_num = models.IntegerField(null=True)
    send_time = models.DateTimeField(null=True)
    Cid = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'user_check'
