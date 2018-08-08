from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
# Create your views here.
def index(request):
    return render(request, "index.html")
# 登录动作
def login_action(request):
    if request.method == 'POST':
        usernam = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(usernam=usernam, password=password)
        if user is not None:
            auth.login(request, user)  #登录
            request.session['user'] = usernam  # 将 session 信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
# 登录成功页
@login_required
def event_manage(requset):
    username = requset.session.get('user', '')    #读取浏览器session
    return render(requset, "event_manage.html", {"user": username})
#发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})
#发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user":username, "events":event_list})
#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果 page 不是整数，取第一页面
        contacts = paginator.page(1)
    except EmptyPage:
        #如果 page 不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})
#签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event,id=eid)
    return render(request, 'sign_index.html', {'event':event})
#签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in seccess!',
                                                   'guest': result})
#退出登录
@login_required()
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response