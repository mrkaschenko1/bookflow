from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from book.models import Tag
from .forms import SignUpForm, ImageUploadForm, TagForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .forms import ProfileForm, UserForm
from .models import Profile, Avatar
from bookflow.constants import DEFAULT_AVATAR


class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "Your account was successfully created"
    template_name = 'signup.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    # Optional (default: 'registration/password_change_form.html')
    # template_name = 'accounts/my_password_change_form.html'
    # Optional (default: `reverse_lazy('password_change_done')`)
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
            # if not avatar_form.cleaned_data['image'].endswith('default_avatar.png'):
            #     avatar = Avatar(image=avatar_form.cleaned_data['image'], profile=profile)
            #     avatar.save()
            # avatar = Avatar(image=avatar_form.cleaned_data['image'], profile=profile)
            # avatar.save()
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
    model = Tag
    template_name = 'accounts/tags.html'
    context_object_name = 'tags'


class CreateCrudTag(View):
    def get(self, request):
        profile = request.user.profile
        title1 = request.GET.get('name', None)

        if Tag.objects.filter(name=title1, profile=profile):
            data = {
                'err': 'You already have tag with this name'
            }
            return JsonResponse(data)
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
