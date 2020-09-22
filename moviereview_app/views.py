from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView, View
from django.views.generic.detail import DetailView
from moviereview_app.models import Category, Article, Comments, UserAccount
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from moviereview_app.forms import (CommentCreationForm, RegistrationForm, LoginForm,
                                   EditUserProfileForm, CategoryCreationForm, ArticleCreationForm)
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


class DisplayArticlesByCategory(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        articles = Article.objects.filter(category__name=category)
        sub_template = render(request, 'category_results.html', {
                              'articles': articles})
        return HttpResponse(sub_template)


class UserReactionView(View):
    template_name = 'category_detail.html'

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('article_id')
        article = Article.objects.get(id=article_id)
        query = request.GET.get('query')
        if query == 'like':
            if request.user not in article.users_reactions.all():
                article.likes += 1
                article.users_reactions.add(request.user)
                article.save()
        elif query == 'dislike':
            if request.user not in article.users_reactions.all():
                article.dislikes += 1
                article.users_reactions.add(request.user)
                article.save()
        data = {
            'total_likes': article.likes,
            'total_dislikes': article.dislikes
        }
        return JsonResponse(data)


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
            return HttpResponseRedirect(reverse('categories_view'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


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


class RemoveArticleFromFavoriteView(View):
    model = UserAccount
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs):
        fav_article = self.model.objects.get(id=id)
        fav_article.remove(id)

        # article_id = request.GET.get('fav_id')
        # article = Article.objects.get(id=article_id)
        return HttpResponseRedirect(reverse('account_view'))


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


class CategoryCreateView(View):
    template_name = 'add_category.html'

    def get(self, request, *args, **kwargs):
        form = CategoryCreationForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CategoryCreationForm(request.POST or None)
        if form.is_valid():
            new_category = form.save(commit=False)
            slug = form.cleaned_data.get('slug')
            description = form.cleaned_data.get('description')
            new_category.save()
            Category.objects.create(name=Category.objects.get(name=new_category.name),
                                    slug=new_category.slug,
                                    description=new_category.description)
            return HttpResponseRedirect(reverse('categories_view'))
        context = {
            'form': None
        }
        return render(request, self.template_name, context)


class ArticleCreateView(View):
    template_name = 'add_article.html'
    model = Article

    def get(self, request, *args, **kwargs):
        form = ArticleCreationForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ArticleCreationForm(request.POST or None)
        if form.is_valid():
            new_article = form.save(commit=False)
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            image = form.cleaned_data.get('image')
            synopsis = form.cleaned_data.get('synopsis')
            category = form.cleaned_data.get('category')
            url_embed = form.cleaned_data.get('url_embed')
            new_article.save()
            self.model.objects.create(title=Article.objects.get(title=new_article.name),
                                      slug=new_article.slug,
                                      image=new_article.image,
                                      synopsis=new_article.synopsis,
                                      category=new_article.category,
                                      url_embed=new_article.url_embed
                                      ),

            return HttpResponseRedirect(reverse('categories_view'))
        context = {
            'form': None
        }
        return render(request, self.template_name, context)


@login_required
def updateProfile(request, user_id):
    if request.method == 'POST':
        form = EditUserProfileForm(data=request.POST, instance=request.user)
        update = form.save(commit=False)
        update.user = request.user
        update.save()
        return render(request, 'user_account.html', {'user': user_id})
        # return HttpResponseRedirect(reverse('account_view'))

    else:
        form = EditUserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
