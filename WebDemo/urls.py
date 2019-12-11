"""WebDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from Web_Demo.views import index,register_user,change_password,test,article,write_blog,add_content,fresh_data,file_upload\
    ,view_blog,my_blog,blog_list,blog_change,edit_blog,weather,userlogout


urlpatterns = [
    url(r"^$",index,name="index"),
    url(r"^userlogout/$", userlogout, name="userlogout"),
    url(r"^register_user/$",register_user, name="register_user"),
    url(r"^article/$", article, name="article"),
    url(r"^change_password/$", change_password, name="change_password"),
    url(r"^write_blog/$", write_blog, name="write_blog"),
    url(r"^weather/$", weather, name="weather"),
    url(r"^test/$", test, name="test"),
    #JS操作
    url(r"^add_content/$", add_content, name="add_content"),
    url(r"^fresh_data/$", fresh_data, name="fresh_data"),
    url(r"^blog_list/$", blog_list, name="blog_list"),
    url(r"^blog_change/$", blog_change, name="blog_change"),
    #上传图片处理
    url(r'^file_upload/', file_upload),
    url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.UPLOAD_ROOT}),
    #特殊路径处理
    path('view_blog/<str:blog_id>',view_blog,name="view_blog"),
    path('my_blog/<str:user>', my_blog, name="my_blog"),
    path('edit_blog/<str:blog_id>', edit_blog, name="edit_blog"),
    #admin
    path('admin/', admin.site.urls),
]
