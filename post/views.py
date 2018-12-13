from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from django.http import HttpResponseNotFound
from user.views import auth
import simplejson
from post.models import Post, Content
import datetime
import math
from user.models import User


@auth
def pub(request: HttpRequest):
    print(request.path)  # post/1
    print(request.body)  # 里面有title，content
    try:
        payload = simplejson.loads(request.body)  # 有title,content
        title = payload['title']
        contents = payload['content']

        post = Post()
        post.title = title  # 往数据库添加title
        post.postdate = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8))
        )  # 时区
        # 实例对实例，id内部来处理,request.user是User一个实例，作者是一个外键
        post.author = request.user  # User(request.user.id)
        post.save()  # save之后就有id了
        content = Content()
        content.post = post
        content.content = contents
        content.save()
        return JsonResponse({
            'post_id': post.id
        })  # 如果正确了，返回post.id
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


# id参数是正则表达式分组号
def get(request: HttpRequest, id):  # /post/1 在request.path中
    print(id, type(id))  # http1.1之前都是文本传输的
    try:
        post = Post.objects.get(pk=int(id))
        return JsonResponse({
            'post': {
                'post_id': post.id,
                'title': post.title,
                'postdate': int(post.postdate.timestamp()),  # 时间对象的时间戳
                'author': post.author.name,
                'author_id': post.author.id,  # post.author_id
                'content': post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


def validate(d: dict, name: str, type_func, default, validate_func):
    try:
        result = type_func(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result


def getall(request: HttpRequest):  # 文章列表页，有title和id,id是编程用
    page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else y)
    size = validate(request.GET, 'size', int, 20, lambda x, y: x if x > 0 and x < 101 else y)
    try:  # 按照id倒排
        start = (page - 1) * size
        posts = Post.objects.order_by('-pk')
        count = posts.count()
        posts = posts[start: start+size]  # 按id降序排
        if posts:

            return JsonResponse({
                'posts': [
                    {
                     'post_id': post.id,
                     'title': post.title
                    }
                    for post in posts
                ], 'pagination': {
                    'page': page,
                    'size': size,
                    'count': count,
                    'pages': math.ceil(count/size)
                }
            })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


# def getall(request: HttpRequest):  # 文章列表页，有title和id,id是编程用
#     try:  # 页码
#         page = int(request.GET.get('page'))
#         page = page if page > 0 else 1
#     except:
#         page = 1
#     try:  # 页码行数
#         # 这个数据不要轻易让浏览器端改变，如果允许改变，一定要控制范围
#         size = int(request.GET.get('size'))
#         size = size if size > 0 and size < 101 else 20
#     except:
#         size = 20
#     try:  # 按照id倒排
#         start = (page - 1) * size
#         posts = Post.objects.order_by('-pk')
#         count = posts.count()
#         posts = posts[start: start+size]  # 按id降序排
#         if posts:
#
#             return JsonResponse({
#                 'post': [
#                     {
#                      'post_id': post.id,
#                      'title': post.title
#                     }
#                     for post in posts
#                 ], 'pagination': {
#                     'page': page,
#                     'size': size,
#                     'count': count,
#                     'pages': math.ceil(count/size)
#                 }
#             })
#     except Exception as e:
#         print(e)
#         return HttpResponseNotFound()





















