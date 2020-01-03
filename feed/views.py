from time import timezone

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

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
    model = Post
    template_name = 'feed/profile_posts.html'
    context_object_name = 'posts'


class CreateCrudPost(View):
    def post(self, request):
        user = request.user
        title1 = request.POST.get('title', None)
        body1 = request.POST.get('body', None)

        # if Post.objects.filter(title=title1, , profile=profile):
        #     data = {
        #         'err': 'You already have tag with this name'
        #     }
        # elif Tag.objects.filter(profile=profile).count() >= TAG_LIMIT:
        #     data = {
        #         'err': 'You have too much tags, can`t be more'
        #     }
        obj = Post.objects.create(
            title=title1,
            body=body1,
            user=user
        )

        post = {'id': obj.id, 'title': obj.title, 'body': obj.body, 'created_at': obj.created_at}

        data = {
            'post': post
        }
        return JsonResponse(data)


class UpdateCrudPost(View):
    def post(self, request):
        user = request.user
        id1 = request.POST.get('id', None)
        title1 = request.POST.get('title', None)
        body1 = request.POST.get('body', None)

        obj = Post.objects.get(id=id1)

        obj.title = title1
        obj.body = body1
        obj.save()
        post = {'id': obj.id, 'title': obj.title, 'body': obj.body, 'created_at': obj.created_at}

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


def pusher_authentication(request):
    channel = request.GET.get('channel_name', None)
    socket_id = request.GET.get('socket_id', None)
    auth = pusher.authenticate(
        channel=channel,
        socket_id=socket_id
    )
    return JsonResponse(json.dumps(auth), safe=False)


def push_feed(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            pusher.trigger(u'a_channel', u'an_event', {u'title': f.title, u'body': f.body})
            return HttpResponse('ok')
        else:
            # return a form not valid error
            return HttpResponse('form not valid')
    else:
        # return error, type isnt post
        return HttpResponse('error, please try again')