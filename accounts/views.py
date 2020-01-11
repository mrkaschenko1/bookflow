from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from book.models import Tag
from .forms import SignUpForm, ImageUploadForm, TagForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .forms import ProfileForm, UserForm
from .models import Profile, Avatar
from bookflow.constants import DEFAULT_AVATAR, TAG_LIMIT


class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "Your account was successfully created"
    template_name = 'signup.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/profile.html'


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        avatar_form = ImageUploadForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid() and avatar_form.is_valid():
            profile = request.user.profile
            # if not (avatar_form.cleaned_data['image']).to_string().endswith('default_avatar.png'):
            try:
                Avatar.objects.get(profile=profile)
                old_avatar = Avatar.objects.get(profile=profile)
                if avatar_form.cleaned_data['image'] != DEFAULT_AVATAR and old_avatar != DEFAULT_AVATAR:
                    old_avatar.delete()
                    avatar = Avatar(image=avatar_form.cleaned_data['image'], profile=profile)
                    avatar.save()
            except:
                pass

            print(avatar_form.cleaned_data['image'])
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        avatar_form = ImageUploadForm(instance=request.user.profile.avatar)
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'avatar_form': avatar_form
    })


@login_required
def delete_pic(request):
    if request.user.profile.avatar.image.url != '/media/default/default_avatar.png':
        profile = request.user.profile
        try:
            Avatar.objects.get(profile=profile)
            old_avatar = Avatar.objects.get(profile=profile)
            old_avatar.delete()
        except:
            pass
        avatar = Avatar(image='default/default_avatar.png', profile=profile)
        avatar.save()
        messages.success(request, 'Avatar deleted successfully')
    else:
        messages.warning(request, 'You don`t have avatar, so you can`t delete it')
    return redirect('update_profile')


@login_required
def index(request):
    return render(request, 'home.html')


class TagCrudView(ListView):
    # model = Tag
    # queryset = Tag.objects.filter(profile=)
    template_name = 'accounts/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        queryset = Tag.objects.filter(profile=self.request.user.profile)
        return queryset


class CreateCrudTag(View):
    def get(self, request):
        profile = request.user.profile
        title1 = request.GET.get('name', None)

        if Tag.objects.filter(name=title1, profile=profile):
            data = {
                'err': 'You already have tag with this name'
            }
        elif Tag.objects.filter(profile=profile).count() >= TAG_LIMIT:
            data = {
                'err': 'You have too much tags, can`t be more'
            }
        else:
            obj = Tag.objects.create(
                name=title1,
                profile=profile
            )

            tag = {'id': obj.id, 'name': obj.name}

            data = {
                'tag': tag
            }
        return JsonResponse(data)


class UpdateCrudTag(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        title1 = request.GET.get('name', None)

        obj = Tag.objects.get(id=id1)
        if Tag.objects.filter(name=title1, profile=request.user.profile).exclude(id=id1):
            data = {
                'err': 'You already have tag with this name, try again'
            }

        else:
            obj.name = title1
            obj.save()
            tag = {'id': obj.id, 'name': obj.name}

            data = {
                'tag': tag
            }
        return JsonResponse(data)


class DeleteCrudTag(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Tag.objects.get(id=id1, profile=request.user.profile).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class ProfileDetailView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        post_list = user.posts.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(post_list, 5)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'accounts/my_profile_info.html', {'user_from_view': user, 'posts': posts})

