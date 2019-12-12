from __future__ import unicode_literals

import json
import os
import random
import time
import datetime
import re

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import loginuser, auth_email, blog_attributes,blog,aphorisms


# Create your views here.

@csrf_exempt
def index(request):
    if request.method == "GET":
        if request.is_ajax():
            return render(request, "../templates/login.html")
        else:
            return redirect("/article/")
    else:
        user = request.POST.get("user")
        password = request.POST.get("password")
        if user != "":
            auth_user  = loginuser.objects.filter(user=user)
            if auth_user:
                if password != "":
                    auth_password = check_password(password,loginuser.objects.get(user=user).password)
                    if auth_password:
                        request.session["username"] = user
                        request.session["password"] = password
                        return JsonResponse({"message": "success","url":"/article/"}, safe=False)
                    else:
                        return JsonResponse({"message": "密码错误!"}, safe=False)
                else:
                    return JsonResponse({"message": "密码不能为空!"}, safe=False)
            else:
                return JsonResponse({"message": "用户名不存在!"}, safe=False)
        else:
            return JsonResponse({"message": "用户名不能为空!"}, safe=False)

def userlogout(request):
    request.session.delete("session_key")
    request.session.clear()
    return HttpResponseRedirect('/article/')

@csrf_exempt
def register_user(request):
    if request.method == "GET":
        Message = {"message": "start"}
        return render(request,'../templates/register_user.html', {"message": json.dumps(Message)})
    else:
        name = request.POST.get("new_name")
        email = request.POST.get("new_email")
        password = request.POST.get("new_password")
        re_password = request.POST.get("new_re_password")
        if password != re_password:
            return JsonResponse({"message": "密码输入不一致"}, safe=False)
        else:
            try:
                loginuser.objects.create(user=name,
                                         email=email,
                                         password=make_password(password),
                                         last_login_time=datetime.datetime.now(),
                                         create_Time=datetime.datetime.now())
                auth_email.objects.create(user=name,email=email)
                request.session["username"] = name
                request.session["password"] = password
                return JsonResponse({"message":"success"},safe=False)
            except BaseException as e:
                return JsonResponse({"message":"%s"%e},safe=False)

@csrf_exempt
def article(request):
    if request.method == "GET":
        bg_path = os.path.join("%s"%settings.STATICFILES_DIRS,"images")
        bg_list = os.listdir(("{0}/{1}").format(bg_path,"blog_bg"))
        num = random.randint(0,len(bg_list)-1)
        blog_content = blog.objects.all()
        for i in blog_content:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', i.content)
            dd.replace(" ","&nbsp")
            i.content = dd
            i.content = i.content.replace("&nbsp;", " ")
        return render(request, '../templates/article.html', {"num":num, "blog_content":blog_content})
    else:
        bg_path = os.path.join("%s"%settings.STATICFILES_DIRS,"images")
        bg_list = os.listdir(("{0}/{1}").format(bg_path,"blog_bg"))
        num = random.randint(0,len(bg_list)-1)
        blog_content = blog.objects.all().order_by("-create_Time")
        for i in blog_content:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', i.content)
            dd.replace(" ","&nbsp")
            i.content = dd
            i.content = i.content.replace("&nbsp;", " ")
        return render(request, '../templates/article_blog.html', {"num":num, "blog_content":blog_content})

def change_password(request):
    return render(request, '../templates/change_password.html')

def write_blog(request):
    if request.method == "GET":
        classification_list = []
        type_list = []
        tag_list = []
        attr = blog_attributes.objects.values()
        if attr == "":
            pass
        else:
            for ele in attr:
                if ele["attribute"] == "classification":
                    classification_list.append(ele["attribute_value"])
                elif ele["attribute"] == "tag":
                    tag_list.append(ele["attribute_value"])
                else:
                    type_list.append(ele["attribute_value"])
        return render(request,'../templates/write_blog.html',{"classification_list":classification_list,
                                                              "type_list":type_list,
                                                              "tag_list":tag_list})
    else:
        tittle = request.POST.get("tittle")
        content = request.POST.get("content")
        tag = request.POST.get("tag")
        classification = request.POST.get("classification")
        type = request.POST.get("type")
        ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        ran_str = ipstamp + timestamp
        blog_id = "blog_%s" % ran_str
        print(content)
        try:
            blog.objects.create(blog_id=blog_id,
                                tittle=tittle,
                                content=content,
                                tag=tag,
                                classification=classification,
                                type=type,
                                subbmiter=request.session["username"],
                                create_Time=datetime.datetime.now(),
                                mod_Time=datetime.datetime.now())
            return redirect('/article/')
        except BaseException as e:
            return JsonResponse({"info":"%s"%e})

def view_blog(request,blog_id):
    blog_content = blog.objects.get(id=blog_id)
    print(blog_content.id)
    view_count = blog_content.view_count
    blog.objects.filter(id=blog_id).update(view_count=view_count+1)
    return render(request,'../templates/view_blog.html',{"blog_content":blog_content})

@csrf_exempt
def my_blog(request,user):
    if request.method == "GET":
        return render(request,'../templates/my_blog.html',{"user":user})

def edit_blog(request,blog_id):
    if request.method == "GET":
        blog_content = blog.objects.get(blog_id=blog_id)
        classification_list = []
        type_list = []
        tag_list = []
        attr = blog_attributes.objects.values()
        if attr == "":
            pass
        else:
            for ele in attr:
                if ele["attribute"] == "classification":
                    classification_list.append(ele["attribute_value"])
                elif ele["attribute"] == "tag":
                    tag_list.append(ele["attribute_value"])
                else:
                    type_list.append(ele["attribute_value"])
        return render(request,'../templates/edit_blog.html',{"blog_content":blog_content,
                                                             "classification_list": classification_list,
                                                             "type_list": type_list,
                                                             "tag_list": tag_list
                                                             })
    else:
        content = request.POST.get("content")
        tag = request.POST.get("tag")
        classification = request.POST.get("classification")
        type = request.POST.get("type")
        try:
            blog_content = blog.objects.get(blog_id=blog_id)
            blog_content.content = content
            blog_content.type = type
            blog_content.tag = tag
            blog_content.classification = classification
            blog_content.save()
            return redirect("/my_blog/"+request.session["username"])
        except BaseException as e:
            print(e)



#测试页面
def test(request):
    bg_path = os.path.join("%s"%settings.STATICFILES_DIRS,"images")
    bg_list = os.listdir(("{0}/{1}").format(bg_path,"blog_bg"))
    num = random.randint(0,len(bg_list)-1)
    blog_content = blog.objects.all()
    for i in blog_content:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', i.content)
        dd.replace(" ","&nbsp")
        i.content = dd
        i.content = i.content.replace("&nbsp;", " ")
    return render(request, '../templates/test.html', {"num":num, "blog_content":blog_content})


#处理JS
@csrf_exempt
def add_content(request):
    choice = request.POST.get("choice")
    content = request.POST.get("content")
    try:
        insert_data = blog_attributes.objects.get_or_create(attribute=choice,attribute_value=content)
        if insert_data[1] == True:
            return JsonResponse({"info": "done"},safe=False)
        else:
            return JsonResponse({"info": "%s已存在"%content},safe=False)
    except BaseException as e:
        return JsonResponse({"info":"%s"%e},safe=False)

@csrf_exempt
def fresh_data(request):
    choice_list = []
    choice = request.POST.get("choice")
    choice_values = blog_attributes.objects.filter(attribute=choice).values("attribute_value")
    for value in choice_values:
        choice_list.append(value["attribute_value"])
    return JsonResponse({"data":choice_list},safe=False)

@csrf_exempt
def blog_list(request):
    orderby = request.POST.get("orderby")
    if orderby == "default":
        user_blog = blog.objects.filter(subbmiter=request.session["username"]).order_by("-create_Time")
        for i in user_blog:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', i.content)
            i.content = dd
            i.content = i.content.replace("&nbsp;", " ")
        return render(request,'../templates/my_blog_template.html',{"user_blog":user_blog})
    elif orderby == "time":
        user_blog = blog.objects.filter(subbmiter=request.session["username"]).order_by("create_Time")
        for i in user_blog:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', i.content)
            i.content = dd
            i.content = i.content.replace("&nbsp;", " ")
        return render(request,'../templates/my_blog_template.html',{"user_blog":user_blog})

@csrf_exempt
def blog_change(request):
    action = request.POST.get("action")
    blog_id = request.POST.get("blog_id")
    if action == "delete":
        try:
            blog.objects.filter(blog_id=blog_id).delete()
            return JsonResponse({"info":"done"},safe=False)
        except BaseException as e:
            return JsonResponse({"info":"%s"%e},safe=False)

@csrf_exempt
def weather(request):
    return render(request,'../templates/weather.html')

def aphorisms_request(request):
    aphorisms_count = len(aphorisms.objects.all().values())
    count = random.randint(1,aphorisms_count)
    aphorisms_content = aphorisms.objects.get(id=count)
    return JsonResponse({"content":aphorisms_content.content,"author":aphorisms_content.author},safe=False)


#处理上传图片函数
@csrf_exempt
def file_upload(request):
    files = request.FILES.get('upload_file')
    name = files.name
    att = name.split(".")[1]
    ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ran_str = ipstamp + timestamp
    file_name = "image_%s.%s"%(ran_str,att)
    file_dir = settings.UPLOAD_ROOT
    file_path = "%s/%s"%(file_dir,file_name)
    if request.method == "POST":
        open(file_path, 'wb+').write(files.read())  # 上传文件
        # 得到JSON格式的返回值
        upload_info = {"success": True, 'file_path': settings.UPLOAD_URL + file_name}
        upload_info = json.dumps(upload_info)
        return HttpResponse(upload_info, content_type="application/json")