from django.shortcuts import render

# Create your views here.

# user/views.py中
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
import simplejson
from .models import User
from django.db.models import Q
import jwt
import bcrypt
from django.conf import settings
import datetime

AUTH_EXPIPE = 8 * 60 * 60


def gen_token(user_id):
    """生成token"""
    key = settings.SECRET_KEY
    # 增加时间戳，判断是否重发token或重新登录
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIPE
    }, key, 'HS256').decode()  # 字符串


# 注册
def reg(request: HttpRequest):
    print(request.body)
    try:
        # 有任何异常，都返回400， 如果保存数据出错，则向外抛出异常
        payload = simplejson.loads(request.body)
        print(type(payload), payload)
        email = payload["email"]
        query = User.objects.filter(email=email)
        print(type(query), '-------------')
        # print(query.query)
        if query.first():  # 如果存在，则return Error
            print('=============')
            return HttpResponseBadRequest("用户名已存在")

        name = payload["name"]
        password = payload["password"]
        print(email)
        print(name)
        print(password)

        user = User()
        user.email = email
        user.name = name
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            user.save()
            # 注册成功，返回token即成功登录
            token = gen_token(user.id)
            res = JsonResponse({
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email
                }, 'token': token
            })
            res.set_cookie('jwt', token)
            return res
            # return JsonResponse({
            #     'user_id': user.id
            # })  # 如果正常，返回json数据
        except Exception as e:
            print(e)
            return JsonResponse({'reason': 'asded'}, status=400)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest("参数错误")


def login(request: HttpRequest):
    print('++++++++++++++++++++++')
    print(request.POST)
    print(request.body)
    print('++++++++++++++++++++++')
    try:
        payload = simplejson.loads(request.body)  # 获取登录信息数据
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                # 验证通过，返回true
                token = gen_token(user.id)
                res = JsonResponse({
                    'user': {
                        'user_id': user.id,
                        'name': user.name,
                        'email': user.email
                    }, 'token': token
                })
                res.set_cookie('jwt', token)

                return res
            else:
                return HttpResponseBadRequest('登录失败1')
        else:
            return HttpResponseBadRequest('登录失败2')

    except Exception as e:  # 有任何异常都返回
        print(e)
        # 这里返回实例，不是异常类
        return HttpResponseBadRequest('登录失败3')


def auth(fn):
    def wrapper(request: HttpRequest):
        # 自定义header jwt
        token = request.META.get('HTTP_JWT', None)  # 会被加前缀HTTP_ 且大写
        print(token)
        if not token:  # None没拿到，认证失败
            return HttpResponseBadRequest('no token')
        key = settings.SECRET_KEY
        try:  # 解码，同时验证过期时间
            payload = jwt.decode(token, key, algorithms=['HS256'])
            print(payload)  # 超过时间Signature has expired
            # user_id = payload.get('user_id', -1)
            # user = User.objects.filter(pk=user_id).get()
            user = User.objects.filter(pk=payload['user_id']).get()
            print(user)
            if user:
                request.user = user  # 如果正确，则注入user
            else:
                return HttpResponseBadRequest('用户名密码错误')
        except jwt.ExpiredSignatureError as e:
            print(e)
            return HttpResponseBadRequest('过期')

        except Exception as e:
            print(e)
            return HttpResponseBadRequest('用户名密码错误')
        ret = fn(request)
        return ret

    return wrapper


@auth
def show(request: HttpRequest):
    print(request.user)
    return JsonResponse({"status": "ok"})


class AuthMiddleware(object):
    def __init__(self, get_response):  # 从内层里面拿到response
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(request, '---------------------')
        print(request.GET)
        print(request.POST)
        print(request.body)
        token = request.META.get('HTTP_JWT', None)
        print(token)
        # 统计ip，1分钟1000次以上
        # 使用字典记录次数=》redis kv
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
