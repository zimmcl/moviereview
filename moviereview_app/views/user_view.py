from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.views.generic.list import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic import UpdateView, CreateView
from moviereview_app.models import Category, Article, Comments, UserAccount
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from moviereview_app.forms import (CommentCreationForm, RegistrationForm, LoginForm,
                                   UserUpdateForm, CategoryCreationForm, ArticleCreationForm,
                                   CategoryUpdateForm, ArticleUpdateForm)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


"""
----------------------------------------------------------------------------
"""


class RegisterUserView(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        #
        form = RegistrationForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            new_user.set_password(password)
            password_check = form.cleaned_data.get('password_check')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            new_user.save()
            UserAccount.objects.create(user=User.objects.get(username=new_user.username),
                                       first_name=new_user.first_name,
                                       last_name=new_user.last_name,
                                       email=new_user.email)
            return HttpResponseRedirect(reverse('login_view'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


"""
----------------------------------------------------------------------------
"""


class LoginUserView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return HttpResponseRedirect(reverse('categories_view'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


"""
----------------------------------------------------------------------------
"""


class UserAccountView(View):
    template_name = 'user_account.html'

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get('user')
        current_user = UserAccount.objects.get(
            user=User.objects.get(username=user))
        context = {
            'categories': Category.objects.all(),
            'user': current_user,
            'all_user': User.objects.all()
        }
        return render(request, self.template_name, context)


"""
----------------------------------------------------------------------------
"""


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'edit_profile.html'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(self.model, pk=self.kwargs['edit_user'])
        return user

    def get_success_url(self, *args, **kwargs):
        user = get_object_or_404(self.model, pk=self.kwargs['current_user'])
        return reverse('account_view', kwargs={'user': user})


"""
----------------------------------------------------------------------------
"""


class UserDeleteView(DeleteView):
    model = User

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""
