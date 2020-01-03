# from django.contrib.auth.models import User
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, DetailView
# from django.views.generic.edit import CreateView, DeleteView
# from newsfeed.models import Tweet, Follow
#
# from stream_django.enrich import Enrich
# from stream_django.feed_manager import feed_manager
#
# enricher = Enrich()
#
#
# class TimelineView(CreateView):
#     fields= ['text']
#     model = Tweet
#     success_url = reverse_lazy('timeline_feed')
#     template_name = 'newsfeed/timeline.html'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(TimelineView, self).form_valid(form)
#
#     def get_context_data(self, form=None):
#         context = super(TimelineView, self).get_context_data()
#
#         feeds = feed_manager.get_news_feeds(self.request.user.id)
#         activities = feeds.get('timeline').get()['results']
#         enriched_activities = enricher.enrich_activities(activities)
#
#         context['activities'] = enriched_activities
#         context['login_user'] = self.request.user
#         context['hashtags'] = Hashtag.objects.order_by('-occurrences')
#
#         return context
#
#
# class HomeView(CreateView):
#     greeting = "Welcome to Stream Twitter"
#
#     def get(self, request, **kwargs):
#         context = {
#             'login_user': request.user,
#             # 'users': User.objects.order_by('id')[:50]
#         }
#         return render(request, 'newsfeed/home.html', context)
#
#
# class FollowView(CreateView):
#     form_class = FollowForm
#     model = Follow
#     success_url = reverse_lazy('timeline_feed')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(FollowView, self).form_valid(form)
#
#
# class UnfollowView(DeleteView):
#     model = Follow
#     success_url = reverse_lazy('timeline_feed')
#
#     def get_object(self):
#         target_id = self.kwargs['target_id']
#         return self.get_queryset().get(target__id=target_id)
#
#
# class DiscoverView(TemplateView):
#     template_name = 'newsfeed/follow_form.html'
#
#     def get_context_data(self):
#         context = super(DiscoverView, self).get_context_data()
#
#         users = User.objects.order_by('date_joined')[:50]
#         following = []
#         for i in users:
#             if len(i.followers.filter(user=self.request.user.id)) == 0:
#                 following.append((i, False))
#             else:
#                 following.append((i, True))
#
#         context['users'] = users,
#         context['form'] = FollowForm()
#         context['login_user'] = self.request.user
#         context['following'] = following
#
#         return context
#
#
# class UserView(DetailView):
#     model = User
#     template_name = 'newsfeed/user.html'
#
#     def get_object(self):
#         return self.get_queryset().get(username=self.kwargs['username'])
#
#     def get_context_data(self, object):
#         user = self.object
#         feeds = feed_manager.get_user_feed(user.id)
#         activities = feeds.get()['results']
#         activities = enricher.enrich_activities(activities)
#
#         return {
#             'activities': activities,
#             'user': user,
#             'login_user': self.request.user
#         }
#
#
# class HashtagView(TemplateView):
#     template_name = 'newsfeed/hashtag.html'
#
#     def get_context_data(self, hashtag):
#         context = super(TemplateView, self).get_context_data()
#
#         hashtag = hashtag.lower()
#         feed = feed_manager.get_feed('user', f'hash_{hashtag}')
#         activities = feed.get(limit=25)['results']
#
#         context['hashtag'] = hashtag
#         context['activities'] = enricher.enrich_activities(activities)
#
#         return context
#
# class TweetView(CreateView):
#     model = Tweet
#     fields = ['text']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(Tweet, self).form_valid(form)