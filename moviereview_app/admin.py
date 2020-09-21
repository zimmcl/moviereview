from django.contrib import admin

from moviereview_app.models import (Category, Article, Comments,
                                    UserAccount)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comments)
admin.site.register(UserAccount)
