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


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(
            *args, **kwargs)
        context['categories'] = Category.objects.all()
        context['article'] = self.get_object()
        context['article_comments'] = self.get_object(
        ).comments.all().order_by('-timestamp')
        context['form'] = CommentCreationForm()
        return context


"""
----------------------------------------------------------------------------
"""


class DisplayArticlesByCategory(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        articles = Article.objects.filter(category__name=category)
        sub_template = render(request, 'category_results.html', {
                              'articles': articles})
        return HttpResponse(sub_template)


"""
This view needs to be fixed
"""


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'add_article.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleUpdateForm
    template_name = 'edit_article.html'

    def get_object(self, *args, **kwargs):
        article = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return article

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""


class ArticleDeleteView(DeleteView):
    model = Article

    def get_success_url(self, *args, **kwargs):
        return reverse('categories_view')


"""
----------------------------------------------------------------------------
"""
