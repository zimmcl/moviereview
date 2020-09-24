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


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(
            *args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['action_articles'] = Article.objects.filter(
            category__name='Accion')
        return context


"""
----------------------------------------------------------------------------
"""


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(
            *args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['category'] = self.get_object()
        context['articles_of_category'] = Article.objects.filter(
            category__name=self.get_object())
        return context


"""
----------------------------------------------------------------------------
"""


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreationForm
    template_name = 'add_category.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""


class CategoryDeleteView(DeleteView):
    model = Category

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = 'edit_category.html'

    def get_object(self, *args, **kwargs):
        category = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return category

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')
