from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ImageUploadForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .forms import ProfileForm, UserForm
from .models import Profile, Avatar


class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "Your account was successfully created"
    template_name = 'signup.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    # Optional (default: 'registration/password_change_form.html')
    #template_name = 'accounts/my_password_change_form.html'
    # Optional (default: `reverse_lazy('password_change_done')`)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/profile.html'




@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            profile = get_object_or_404(Profile, pk=request.user.id)
            try:
                Avatar.objects.get(profile=profile)
                old_avatar = Avatar.objects.get(profile=profile)
                old_avatar.delete()
            except:
                pass
            avatar = Avatar(image=form.cleaned_data['image'], profile=profile)
            avatar.save()
            messages.success(request, 'Avatar changed!')
            return redirect('home')
    else:
        form = ImageUploadForm()
    return render(request, 'accounts/avatar.html', {
                  'form': form,
    })