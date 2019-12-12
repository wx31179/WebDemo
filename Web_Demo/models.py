from django.db import models

# Create your models here.

class loginuser(models.Model):
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,null=True)
    last_login_time = models.DateTimeField("最后登录时间")
    create_Time = models.DateTimeField("创建时间")

class auth_email(models.Model):
    user = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,null=True)
    is_auth = models.IntegerField(default=False)
    auth_code = models.CharField(max_length=6,null=True)

class blog_attributes(models.Model):
    attribute = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)

class blog(models.Model):
    blog_id = models.CharField(max_length=100)
    tittle = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=100,null=True)
    classification = models.CharField(max_length=100,null=True)
    subbmiter = models.CharField(max_length=100)
    create_Time = models.DateTimeField("创建时间")
    mod_Time = models.DateTimeField('最后修改时间', auto_now=True)
    view_count = models.IntegerField(default=0)
    applaud_count = models.IntegerField(default=0)

class aphorisms(models.Model):
    content = models.CharField(max_length=100)
    author = models.CharField(max_length=100)