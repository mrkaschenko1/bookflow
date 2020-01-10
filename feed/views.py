from time import timezone

from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from book.models import BookInfo
from .forms import *
from pusher import Pusher
import json

pusher = Pusher(
  app_id='925079',
  key='4ac5984fc15d8ee1ba9a',
  secret='3e2b790de10f27457a7a',
  cluster='eu'
)


class PostCrudView(ListView):
    template_name = 'feed/profile_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


class CreateCrudPost(View):
    def post(self, request):
        user = request.user
        title1 = request.POST.get('title', None)
        body1 = request.POST.get('body', None)
        books1 = request.POST.getlist('books[]', None)

        obj = Post.objects.create(
            title=title1,
            body=body1,
            user=user
        )

        # print("!!!!!!!!!1")
        # print(books1)
        # print("!!!!!!!!!1")

        if books1 is not None:
            for book in books1:
                bookObj = BookInfo.objects.get(id=book)
                obj.books.add(bookObj)

        obj.save()
        pusher.trigger(f'{request.user.username}-channel', 'post-pub', {'message': 'pub posted notification'})

        # books = {}
        books = serializers.serialize("json", obj.books.all())
        print(books)

        post = {'id': obj.id, 'title': obj.title, 'body': obj.body, 'created_at': obj.created_at, 'books': books}

        data = {
            'post': post
        }
        return JsonResponse(data)


class UpdateCrudPost(View):
    def post(self, request):
        id1 = request.POST.get('id', None)
        title1 = request.POST.get('title', None)
        body1 = request.POST.get('body', None)
        checker1 = request.POST.get('checker', None)
        # print(type(checker1))


        obj = Post.objects.get(id=id1)

        obj.title = title1
        obj.body = body1

        if checker1 == 'false':
            books1 = request.POST.getlist('books[]', None)
            obj.books.clear()
            if books1 is not None:
                print(books1)
                for book in books1:
                    bookObj = BookInfo.objects.get(id=book)
                    obj.books.add(bookObj)

        obj.save()
        books = serializers.serialize("json", obj.books.all())

        print(books)
        post = {'id': obj.id, 'title': obj.title, 'body': obj.body, 'created_at': obj.created_at, 'books': books}

        data = {
            'post': post
        }
        return JsonResponse(data)


class DeleteCrudPost(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Post.objects.get(id=id1, user=request.user).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

# def index(request):
#     # get all current posts ordered by the latest
#     all_documents = Post.objects.all().order_by('-id')
#     # return the index.html template, passing in all the feeds
#     return render(request, 'index.html', {'all_documents': all_documents})


# def pusher_authentication(request):
#     channel = request.GET.get('channel_name', None)
#     socket_id = request.GET.get('socket_id', None)
#     auth = pusher.authenticate(
#         channel=channel,
#         socket_id=socket_id
#     )
#     return JsonResponse(json.dumps(auth), safe=False)
#
#
# def push_feed(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             f = form.save()
#             pusher.trigger(u'a_channel', u'an_event', {u'title': f.title, u'body': f.body})
#             return HttpResponse('ok')
#         else:
#             # return a form not valid error
#             return HttpResponse('form not valid')
#     else:
#         # return error, type isnt post
#         return HttpResponse('error, please try again')


class PostList(ListView):
    template_name = 'feed/post_list.html'
    queryset = Post.objects.all().order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 7


class PostLikeToggle(View):
    def get(self, request):
        try:
            id1 = request.GET.get('id', None)
            # print(id1)
            post = Post.objects.get(id=id1)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                post.save()
                print("like removed")
                data = {'status': 'unlike', 'count': post.likes.count()}
            else:
                post.likes.add(request.user)
                post.save()
                print("liked")
                data = {'status': 'like', 'count': post.likes.count()}
        except Exception as e:
            print(e)
            data = {'err': 'Try to update page, this post may be deleted'}
        return JsonResponse(data)