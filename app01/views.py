from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib import auth
# from app01.myform import User as FUser
# from app01.models import User
from app01.models import Account,TMessage,Message,Expert,Collect,Feedback,Identify,Hotspot
from django.contrib import messages
from django import forms
from django.core.mail import send_mail, send_mass_mail
import datetime
import uuid
import hashlib
from login import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.


class UserInfo(forms.Form):
    user_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(error_messages={'required':u'两次密码不一致'},widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField()
    tel = forms.CharField()

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            self.password2 = None
        return self.cleaned_data


def index(request):
    dic = {}
    user_id = request.session.get('user_id', False)
    dic['user_id'] = user_id
    res = Hotspot.objects.order_by('-num')
    dic['hotspot1'] = res[0].keyword
    dic['hotspot2'] = res[1].keyword
    dic['hotspot3'] = res[2].keyword
    dic['hotspot4'] = res[3].keyword
    dic['hotspot5'] = res[4].keyword
    dic['hotspot6'] = res[5].keyword
    dic['href1'] = '/search/?q=' + res[0].keyword
    dic['href2'] = '/search/?q=' + res[1].keyword
    dic['href3'] = '/search/?q=' + res[2].keyword
    dic['href4'] = '/search/?q=' + res[3].keyword
    dic['href5'] = '/search/?q=' + res[4].keyword
    dic['href6'] = '/search/?q=' + res[5].keyword
    return render(request, 'app01/index.html', dic)


# 显示页面


def loginView(request):
    user_id = request.session.get('user_id', False)
    print(user_id)
    if not user_id:
        return render(request, 'app01/login.html')
    else:
        return HttpResponseRedirect('/index/')


def registerView(request):
    user_id = request.session.get('user_id', False)
    print(user_id)
    if not user_id:
        return render(request, 'app01/register.html')
    else:
        return HttpResponseRedirect('/index/')


def userinfoView(request,user_id):
    my_user_id= request.session.get('user_id', False)
    result = Account.objects.filter(user_id=user_id)
    if not result.exists():
        messages.success(request, "异常错误，返回首页")
        return HttpResponseRedirect('/index/')
    # print(user)
    return render(request, 'app01/userinfo.html', {'data': result[0], 'user_id': my_user_id})


# 注册
def register(request):
    obj = UserInfo()
    if request.method == 'POST':
        # user_input_obj = UserInfo(request.POST)
        # if user_input_obj.is_valid():
        user_name = request.POST['user_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        tel = request.POST['tel']
        basic_info = request.POST['basic_info']
        if password1 != password2:
            messages.success(request, "密码不一致！")
            return render(request, 'app01/register.html')
        if Account.objects.filter(user_name=user_name):
            messages.success(request, "用户名重复！")
            return render(request, 'app01/register.html')
        account = Account(user_name=user_name, password=password1, email=email, tel=tel, basic_info=basic_info)
        account.save()
        check = True
        result = Account.objects.filter(user_name=user_name, password=password1)  # filter
        result = result[0]
        request.session['user_id'] = result.user_id  # 修改了
        request.session['user_name'] = result.user_name
        messages.success(request, "注册成功")
        return HttpResponseRedirect('/index/')
        # else:
        #     error_msg = user_input_obj.errors
        #     messages.success(request, error_msg)
        #     return render(request,'app01/login.html',{'obj':user_input_obj,'errors':error_msg})
    return render(request, 'app01/login.html', {'obj': obj})
    # check = False
    # if request.method == 'POST':
    #     form = app01(request.POST)
    #     if form.is_valid():
    #         # print(form.cleaned_data)
    #         user = app01(**form.cleaned_data)
    #         user.save()
    #         check = True
    #         return render(request, 'app01/immediate.html',{'check':check})
    #
    # return HttpResponseRedirect('/index/')


# 登录
def login(request):

    user = request.POST['user_name']
    password = request.POST['password']

    result = Account.objects.filter(user_name=user, password=password)  # filter

    if not result.exists():
        messages.success(request, "用户名或密码不正确！")
        return HttpResponseRedirect('/registerView/')
    else:
        result = result[0]
        request.session['user_id'] = result.user_id #修改了
        request.session['user_name'] = result.user_name
        return HttpResponseRedirect('/index/')


# 注销
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


# def search(request):
#      str = request.POST.get('search_string')
#
#    return HttpResponseRedirect('https://www.baidu.com', str)


def message(request):
    user_id = request.session.get('user_id', False)
    print(user_id)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    result = TMessage.objects.filter(receive_id=user_id).order_by('-send_date')
    result2 = Message.objects.filter(receive=user_id).order_by('-send_date')
    unread1 = 0
    unread2 = 0
    for msg in result:
        if msg.state == 1:
            unread1 += 1
            msg.state = 0
            msg.save()
    for msg in result2:
        if msg.state == 1:
            unread2 += 1
            msg.state = 0
            msg.save()
    return render(request, 'app01/message.html', {'data': result, 'data2': result2, 'user_id': user_id, 'unread1': unread1, 'unread2': unread2})


def sendmessage(request):
    user_id = request.session.get('user_id', False)
    print(user_id)
    if not user_id:
        return render(request, 'app01/login.html')
    return render(request,"app01/sendmessage.html", {'user_id':user_id})


def send(request):
    user = request.POST['user_name']
    content = request.POST['content']
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    receiver = Account.objects.filter(user_name=user)
    if not receiver.exists():
        messages.success(request, "收信人不合法！")
        return HttpResponseRedirect('/sendmessage/')
    user = Account.objects.get(user_id=user_id)
    msg = Message(send=user,receive=receiver[0],content=content,send_date=datetime.datetime.now(),send_name=user.user_name)
    msg.save()
    messages.success(request, "发送成功！")
    return HttpResponseRedirect('/sendmessage/')


def feedback(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    return render(request,'app01/feedback.html',{'user_id': user_id})


def sendfeedback(request):
    content = request.POST['content']
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    # user = Account.objects.get(user_id=user_id)
    msg = Feedback(send=user_id, content=content, send_date=datetime.datetime.now())
    msg.save()
    messages.success(request, "发送成功！")
    return HttpResponseRedirect('/feedback/')


def customerps(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    else:
        result = Account.objects.filter(user_id=user_id)
        result=result[0]
        dic={}
        dic['user_name']=result.user_name
        dic['real_name'] = result.real_name
        dic['tel'] = result.tel
        dic['email'] = result.email
        dic['basic_info'] = result.basic_info
        dic['money'] = result.money
        dic['user_id'] = user_id
        dic['collect'] = Collect.objects.filter(user_id=user_id)
        dic['type'] = result.type
        return render(request,"app01/personal/CustomerPS.html",dic)


def expertps(request):
    return render(request,"app01/personal/ExpertPS.html")

def personalmodify(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        HttpResponseRedirect('/registerView/')
    else:
        result = Account.objects.filter(user_id=user_id)
        result = result[0]
        dic = {}
        dic['user_name'] = result.user_name
        dic['real_name'] = result.real_name
        dic['tel'] = result.tel
        dic['email'] = result.email
        dic['basic_info'] = result.basic_info
        dic['user_id'] = user_id
        return render(request, "app01/personal/PersonalModify.html", dic)


def personalchange(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    else:
        account = Account.objects.get(user_id=user_id)
        account.user_name=request.POST['user_name']
        account.real_name=request.POST['real_name']
        account.tel=request.POST['tel']
        account.email=request.POST['email']
        account.basic_info=request.POST['basic_info']
        account.save()
        messages.success(request, "个人信息修改成功")
        return HttpResponseRedirect("/PS/")


def recharge(request):
    return render(request,"app01/recharge.html")


def expert(request,expert_id):
    user_id = request.session.get('user_id', False)
    result = Expert.objects.filter(expert_id=expert_id)
    if not result.exists():
        return HttpResponseRedirect('/index/')
    return render(request,"app01/personal/Expert.html",{'data': result[0], 'user_id': user_id})


def topup(request):
    return render(request,"app01/TopUp.html")

#


def identify(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    return render(request,"app01/identify/identify.html",{'user_id': user_id})


def confirmM(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    return render(request,"app01/identify/confirmM.html",{'user_id': user_id})


def confirmI(request):
    return render(request,"app01/identify/confirmI.html")


def confirminfo(request,str):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    if str == request.session.get('random_str', False):
        return render(request, "app01/identify/confirminfo.html",{'user_id': user_id})
    else:
        return HttpResponseRedirect('/index/')


def success(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    name = request.POST['name']
    institute = request.POST['institute']
    position = request.POST['position']
    direction = request.POST['direction']
    email = request.POST['email']
    introduction = request.POST['introduction']
    identify_data = Identify(identify_user=user_id,name=name,institute=institute,position=position,direction=direction,email=email,introduction=introduction,time=datetime.datetime.now())
    identify_data.save()
    msg = TMessage(receive_id=user_id,request_id=identify_data.id,content="申请审核中，请耐心等待。",request_date=identify_data.time,send_date=datetime.datetime.now(),type="info",state=1)
    msg.save()
    return render(request,"app01/identify/success.html")


def send_my_email(request):
    title = "ischolar专家认证"
    random_str = str(get_random_str())
    request.session['random_str'] = random_str
    request.session['email'] = request.POST['email']
    msg = "感谢您申请认证，请通过申请时的ip前往： http://127.0.0.1:8000/confirminfo/"
    msg2 = msg+random_str

    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        request.POST['email']
        # 'y1jiaoao@163.com'
    ]
    # 发送邮件
    try:
        send_mail(title, msg2, email_from, reciever)
    except:
        return HttpResponse("发送邮件异常，请重新操作。")
    return HttpResponse("请点击邮件中链接来进入下一步认证（请不要登出账号）。")


def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()
