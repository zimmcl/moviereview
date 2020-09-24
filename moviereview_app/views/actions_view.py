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


class CreateCommentView(View):
    template_name = 'article_detail.html'

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        comment = request.POST.get('comment')
        comment = Comments(author=request.user, comment=comment)
        comment.save()
        new_post_template = render(
            request, 'new_post.html', {'comment': comment})
        article = Article.objects.get(id=article_id)
        article.comments.add(comment)
        article.save()
        return HttpResponse(new_post_template)


"""
----------------------------------------------------------------------------
"""


class UserReactionView(View):
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('article_id')
        article = Article.objects.get(id=article_id)
        stars = request.GET.get('query')
        if request.user not in article.users_reactions.all():
            article.ranking = (article.ranking * article.votes)
            if stars == 'one-star':
                article.ranking += 1
            elif stars == 'two-star':
                article.ranking += 2
            elif stars == 'three-star':
                article.ranking += 3
            elif stars == 'four-star':
                article.ranking += 4
            elif stars == 'five-star':
                article.ranking += 5

            article.votes += 1

            article.users_reactions.add(request.user)
            article.ranking = (article.ranking / article.votes)
            article.save()

        data = {
            'total_stars': article.votes
        }
        return JsonResponse(data)


"""
----------------------------------------------------------------------------
"""


class AddArticlesToFavoutitesView(View):
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs):
        user = UserAccount.objects.get(user=request.user)
        article_id = request.GET.get('article_id')
        article = Article.objects.get(id=article_id)
        if not article in user.favourite_articles.all():
            user.favourite_articles.add(article)
            user.save()
        return JsonResponse({})


"""
Works, but needs to be fixed using class.
"""


def ArticleFavoriteDeleteView(request, user_id, article_id):
    user = get_object_or_404(UserAccount, pk=user_id)
    article = get_object_or_404(Article, pk=article_id)
    context = {'user': user}
    if article in user.favourite_articles.all():
        user.favourite_articles.remove(article)
        user.favourite_articles.all()
    sub_template = render(request, 'user_account.html', context)
    return HttpResponse(sub_template)


"""
----------------------------------------------------------------------------
"""


class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        founded_articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(synopsis__icontains=query))
        context = {
            'categories': Category.objects.all(),
            'founded_articles': founded_articles
        }
        return render(request, self.template_name, context)
