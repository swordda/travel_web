import datetime
import arrow
from django.template import loader
import random
import json
import smtplib
from django.db.models import Max
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from tweb.models import City, Snack, ScenicZone, User, UserCheck
import datetime
import EmailSender


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            print(json_data)
            try:
                user_object = User.objects.get(Uemail=json_data['content'])
                print(user_object.Uname, user_object.Upwd, json_data['password'], '124545')
                if user_object.Upwd == json_data['password']:
                    print(user_object.Upwd)
                    return JsonResponse({"message": "1"})
                else:
                    return JsonResponse({"message": "3"})
            except User.DoesNotExist:
                return JsonResponse({"message": "2"})
        except:
            print(json_data['content'])
            return JsonResponse({"message": "4"})


def sign(request):
    return render(request, 'sign.html')


def sz(request):
    if request.method == 'GET':
        sz_obiect = ScenicZone.objects.get(SZid=request.GET.get('sz'))
        context = {'sz': sz_obiect.SZ_name,
                   'sz_time': sz_obiect.SZ_time,
                   'sz_address': sz_obiect.SZ_address,
                   'sz_pic_url': sz_obiect.SZ_pic_url,
                   'sz_introduce': sz_obiect.SZ_introduce,
                   'sz_score': sz_obiect.SZ_score,
                   'sz_popularity': sz_obiect.SZ_popularity}
        template = loader.get_template('sz.html')
        html_content = template.render(context, request)
        return HttpResponse(html_content, content_type='text/html')


def scity(request):
    if request.method == 'GET':
        try:
            print(request.GET.get('city'))
            city_obiect = City.objects.get(Cname=request.GET.get('city'))
            print('123')
            try:
                sz_object = ScenicZone.objects.filter(SZ_city=city_obiect.Cname).order_by('-SZ_popularity')
                print('234')
                context = {'city': request.GET.get('city'),
                           'data': [],
                           'data2': []}
                print(sz_object)
                for so in sz_object:
                    if so.SZ_name == '':
                        continue
                    print(1)
                    context['data'].append({'sz_name': so.SZ_name, 'sz_score': so.SZ_score, 'sz_pic_url': so.SZ_pic_url,
                                            'sz_sIntroduce': so.SZ_sIntroduce, 'sz_popu': so.SZ_popularity,
                                            'sz_url': 'http://127.0.0.1:8000/sz/?sz=' + str(so.SZid)})
                    print('http://127.0.0.1/sz/?sz=' + str(so.SZid))
                sn_object = Snack.objects.filter(S_city=request.GET.get('city'))
                for sn in sn_object:
                    if sn == '<empty>':
                        continue
                    context['data2'].append(
                        {'sn_name': sn.S_name, 'sn_pic_url': sn.S_pic_url, 'sn_sIntroduce': sn.S_Introduce})
                template = loader.get_template('city.html')
                print(2)
                html_content = template.render(context, request)
                return HttpResponse(html_content, content_type='text/html')
            except ScenicZone.DoesNotExist:
                return JsonResponse({"message": "3"})
        except City.DoesNotExist:
            return JsonResponse({"message": "2"})


def index(request):
    if request.method == 'GET':
        try:
            print(request)
            try:
                user_object = User.objects.get(Uemail=request.GET.get('content'))
                print(user_object.Uname, user_object.Upwd, request.GET.get('password'), '124545')
                if user_object.Upwd == request.GET.get('password'):
                    print(user_object.Upwd)
                    context = {'username': user_object.Uname}
                    print(1)
                    template = loader.get_template('index.html')
                    print(2)
                    html_content = template.render(context, request)
                    print(3)
                    return HttpResponse(html_content, content_type='text/html')
                else:
                    return JsonResponse({"message": "3"})
            except User.DoesNotExist:
                return JsonResponse({"message": "2"})
        except:
            return JsonResponse({"message": "4"})
        # 　return render(request, 'login.html')
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            print(json_data)
            try:
                user_object = User.objects.get(Uemail=json_data['content'])
                print(user_object.Uname, user_object.Upwd, json_data['password'], '124545')
                if user_object.Upwd == json_data['password']:
                    print(user_object.Upwd)
                    return JsonResponse({"message": "1"})
                    # context = {'username': user_object.Uname}
                    # return render(request, 'index.html', context)
                else:
                    return JsonResponse({"message": "3"})
            except User.DoesNotExist:
                return JsonResponse({"message": "2"})
        except:
            print(json_data['content'])
            return JsonResponse({"message": "4"})


def mail(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        rnum = random.randint(100000, 999999)
        try:
            EmailSender.Send('来自旅游产品分析系统的验证码', '你的验证码是：' + str(rnum) + '，请在5分钟内完成注册', json_data['content'])
        except smtplib.SMTPException as e:
            print('error ', e)  # 打印错误
            return JsonResponse({'message': '2'})
        try:
            UserCheck.objects.create(email=json_data['content'], check_num=rnum, send_time=datetime.datetime.now())
        except:
            return JsonResponse({'message': '3'})
        return JsonResponse({'message': '1'})


def signup(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        try:
            max_cid_object = UserCheck.objects.filter(email=json_data['content']).aggregate(Max('Cid'))
        except:
            return JsonResponse({'message': '2'})
        if max_cid_object['Cid__max']:
            user_obj = UserCheck.objects.get(Cid=max_cid_object['Cid__max'])
            if str(user_obj.check_num) == json_data['check']:
                d1 = arrow.now()
                ct = (d1 - user_obj.send_time).total_seconds() + 28800
                if ct < 300:
                    try:
                        e_obj = User.objects.get(Uemail=json_data['content'])
                        return JsonResponse({'message': '4'})
                    except User.DoesNotExist:
                        rid = random.randint(1000000, 99999999)
                        try:
                            User.objects.create(Uname='用户' + str(rid), Uemail=json_data['content'],
                                                Upwd=json_data['password'], jurisdiction='user')
                        except:
                            return JsonResponse({'message': '3'})
                        return JsonResponse({'message': '1'})
                else:
                    return JsonResponse({'message': '2'})
            else:
                return JsonResponse({'message': '2'})
