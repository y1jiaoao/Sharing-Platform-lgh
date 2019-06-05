from django.shortcuts import render,HttpResponseRedirect,reverse
from django.contrib import auth
from django.http import HttpResponse
# from app01.myform import User as FUser
# from app01.models import User
from app01.models import Essay,Patent,Expert,Collect,Comment,Account,Hotspot
from django.contrib import messages
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.


def essayView(request,paper_id):
    # paper_id = request.GET['paper_id']
    result = Essay.objects.filter(paper_id=paper_id)
    if not result.exists():
        return HttpResponseRedirect('/index/')
    else:
        result = result[0]

        click = Essay.objects.get(paper_id=paper_id)
        click.clicks = result.clicks + 1
        click.save()
        str = result.keywords
        str = str.split(";", str.count(';'))
        for i in str:
            if i == '':
                continue
            res = Hotspot.objects.filter(keyword=i)
            if not res.exists():
                add = Hotspot(keyword=i, num=1)
                add.save()
            else:
                res = res[0]
                num = res.num + 1
                Hotspot.objects.filter(keyword=i).update(num=num)
        # paper={}
        # paper['name']=result.paper_name
        # paper['author']=result.author_name
        # paper['introduction'] = result.introduction
        # paper['institute']=result.institute
        # paper['source'] = result.source
        # paper['keywords'] = result.keywords
        # paper['clicks'] = result.clicks
        # paper['db'] = result.db
        # paper['cssci'] = result.cssci
        # paper['download_link'] = result.download_link
        # paper['published_time'] = result.published_time
        # paper['user_id'] = request.session.get('user_id',False)
        paper = result
        user_id = request.session.get('user_id', False)
        is_collect = Collect.objects.filter(user_id=user_id,collection_id=paper_id,type="essay").exists()
        comment_list = Comment.objects.filter(resource_id=paper_id,type="essay").order_by("-comment_date")
        return render(request, 'app01/viewEssay.html', {'paper': paper, 'user_id': user_id, 'is_collect': is_collect, 'comment_list': comment_list})


def expertView(request):
    expert_id = request.GET['expert_id']
    result = Expert.objects.filter(expert_id=expert_id)

    if not result.exists():
        messages.success(request, "目标不存在！")
        return HttpResponseRedirect('expert/')
    else:
        return HttpResponse("<h1>"+result[0].name+"</h1><h2>"+result[0].position+"</h2><h3>"+result[0].institute+"</h3><h4>"+result[0].direction+"</h3><h4>"+result[0].contact+"</h4><p>"+result[0].introduction+"</p>")


def patentView(request,patent_id):
    # patent_id = request.GET['patent_id']
    result = Patent.objects.filter(patent_id=patent_id)

    if not result.exists():
        return HttpResponseRedirect('/index/')
    else:
        result = result[0]

        click = Patent.objects.get(patent_id=patent_id)
        click.clicks = result.clicks + 1
        click.save()

        # apatent={}
        # apatent['name']=result.patent_name
        # apatent['author']=result.author_name
        # apatent['introduction'] = result.introduction
        # apatent['clicks'] = result.clicks
        # apatent['app_number']=result.app_num
        # apatent['app_date']=result.app_date
        # apatent['publish_number'] = result.public_number
        # apatent['published_time'] = result.published_time
        # apatent['source'] = result.source
        # apatent['appliant'] = result.appliant
        # apatent['address'] = result.address
        # apatent['agency'] = result.agency
        # apatent['agent'] = result.agent
        # apatent['main_cls_num']=result.main_cls_num
        # apatent['patent_cls_num']=result.patent_cls_num
        # apatent['code']=result.code
        # apatent['page']=result.page
        # # apatent['download_link'] = result.download_link
        # apatent['user_id'] = request.session.get('user_id',False)
        apatent = result
        user_id = request.session.get('user_id', False)
        is_collect = Collect.objects.filter(user_id=user_id, collection_id=patent_id, type="patent").exists()
        comment_list = Comment.objects.filter(resource_id=patent_id, type="patent").order_by("-comment_date")
        return render(request, 'app01/viewPatent.html', {'apatent': apatent, 'user_id': user_id, 'is_collect': is_collect, 'comment_list': comment_list})


def collect(request,type,id):
    user_id = request.session.get('user_id', False)
    print(user_id)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    result = Collect.objects.filter(user_id=user_id,collection_id=id,type=type)
    if not result.exists():
        if type == "essay":
            collection_name = Essay.objects.get(paper_id=id).paper_name
        elif type == "patent":
            collection_name = Patent.objects.get(patent_id=id).patent_name
        else:
            collection_name = ""
        info = Collect(user_id=user_id,collection_id=id,collection_name=collection_name,type=type)
        info.save()
        messages.success(request, "已收藏！")
    else:
        result[0].delete()
        messages.success(request, "已取消收藏！")
    if type == "essay":
        return HttpResponseRedirect(reverse(type, kwargs={'paper_id': id}))
    elif type == "patent":
        return HttpResponseRedirect(reverse(type, kwargs={'patent_id': id}))
    else:
        return HttpResponseRedirect("index")


def comment(request,type,id):
    user_id = request.session.get('user_id', False)
    if not user_id:
        return HttpResponseRedirect('/registerView/')
    user_name = Account.objects.get(user_id=user_id).user_name
    content = request.POST['content']
    acomment = Comment(type=type,comment_name=user_name,resource_id=id,comment_date=datetime.datetime.now(),content=content)
    acomment.save()
    messages.success(request, "评论成功！")
    if type == "essay":
        return HttpResponseRedirect(reverse(type, kwargs={'paper_id': id}))
    elif type == "patent":
        return HttpResponseRedirect(reverse(type, kwargs={'patent_id': id}))
    else:
        return HttpResponseRedirect("/index/")
