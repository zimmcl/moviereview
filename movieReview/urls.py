"""movieReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from moviereview_app.views.actions_view import (SearchView, AddArticlesToFavoutitesView,
                                                CreateCommentView, UserReactionView, ArticleFavoriteDeleteView)
from moviereview_app.views.category_view import (CategoryListView, CategoryDetailView, CategoryCreateView,
                                                 CategoryDeleteView, CategoryUpdateView)
from moviereview_app.views.article_view import (ArticleDetailView, DisplayArticlesByCategory,
                                                ArticleCreateView, ArticleUpdateView, ArticleDeleteView)
from moviereview_app.views.user_view import (RegisterUserView, LoginUserView, UserAccountView,
                                             UserUpdateView, UserDeleteView)
from django.contrib import admin
from django.urls import path, re_path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.conf.urls.static import static
from django.conf import settings
from moviereview_app import views


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^$', CategoryListView.as_view(), name='categories_view'),

    re_path(r'^category/(?P<slug>[-\w]+)/$',
            CategoryDetailView.as_view(), name='category_detail_view'),

    re_path(r'^search/$', SearchView.as_view(), name='search_view'),

    re_path(r'^article/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
            ArticleDetailView.as_view(), name='article_detail_view'),

    re_path(r'^add_comment/$', CreateCommentView.as_view(),
            name='create_comment_view'),

    re_path(r'^add_article_to_favourites/$', AddArticlesToFavoutitesView.as_view(),
            name='add_article_to_favourites_view'),

    re_path(r'^send_votes/$', UserReactionView.as_view(),
            name='user_reaction_view'),

    re_path(r'^display_articles_by_category/$', DisplayArticlesByCategory.as_view(),
            name='display_articles_by_category_view'),

    re_path(r'^sign_up/$', RegisterUserView.as_view(),
            name='registration_view'),

    re_path(r'^sign_in/$', LoginUserView.as_view(), name='login_view'),

    re_path(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('categories_view')),
            name='logout_view'),

    re_path(r'^change_password/$', PasswordChangeView.as_view(
        success_url=reverse_lazy('categories_view')), name='change_password_view'),

    re_path(r'^user/(?P<user>[-\w]+)/$',
            UserAccountView.as_view(), name='account_view'),

    # Works, but needs to be Fixed.
    re_path(r'^favorite_delete/(?P<user_id>[-\w]+)/(?P<article_id>[-\w]+)/$',
            ArticleFavoriteDeleteView, name='favorite_delete_view'),

    re_path(r'^update_profile/(?P<current_user>[-\w]+)/(?P<edit_user>[-\w]+)/$',
            UserUpdateView.as_view(), name='user_edit_profile'),

    re_path(r'^add_category/$', CategoryCreateView.as_view(),
            name='category_create_view'),

    # Works, but needs to be Fixed.
    re_path(r'^add_article/$', ArticleCreateView.as_view(),
            name='article_create_view'),

    re_path(r'^delete_category/(?P<pk>[-\w]+)/$', CategoryDeleteView.as_view(),
            name='category_delete_view'),

    re_path(r'^update_category/(?P<pk>[-\w]+)/$', CategoryUpdateView.as_view(),
            name='category_update_view'),

    re_path(r'^update_article/(?P<pk>[-\w]+)/$', ArticleUpdateView.as_view(),
            name='article_update_view'),

    re_path(r'^delete_user/(?P<pk>[-\w]+)/$', UserDeleteView.as_view(),
            name='user_delete_view'),

    re_path(r'^delete_article/(?P<pk>[-\w]+)/$', ArticleDeleteView.as_view(),
            name='article_delete_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
