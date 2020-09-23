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


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(
            *args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['carousel_articles'] = Article.objects.all().order_by(
            '-time_added')[:3]
        context['action_articles'] = Article.objects.filter(
            category__name='Accion')
        context['hot_articles'] = Article.objects.all().order_by(
            '-time_added')[:6]
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


class DisplayArticlesByCategory(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        articles = Article.objects.filter(category__name=category)
        sub_template = render(request, 'category_results.html', {
                              'articles': articles})
        return HttpResponse(sub_template)


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


class RegisterUserView(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
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
            # return render(request, 'index.html', {'user': username})
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
            'all_user': User.objects.all
        }
        return render(request, self.template_name, context)


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
This view needs to be fixed 
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


class UserDeleteView(DeleteView):
    model = User

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
