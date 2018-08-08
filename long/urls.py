"""long URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sign import views  # 导入 sign 应用 views 文件

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),  # 添加 index/ 路径
    url(r'^login_action/$', views.login_action),  # 添加登录 路径
    url(r'^event_manage/$', views.event_manage),  # 添加登录成功页路径
    url(r'^accounts/login/$', views.index),
    url(r'^search_name/$', views.search_name),  # 添加发布会搜索表单
    url(r'^guest_manage/$', views.guest_manage),  #添加嘉宾路径
    url(r'^event_index/(?P<eid>[0-9]+)/$', views.event_index), #签到页面路径的路由
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$', views.sign_index_action),#签到动作路径
    url(r'^logout/$', views.logout),   #退出路径
]
