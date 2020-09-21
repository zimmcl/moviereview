from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail_view', kwargs={'slug': self.slug})


def generate_filename(instance, filename):
    filaname = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    image = models.ImageField(upload_to=generate_filename)
    url_embed = models.URLField(max_length=100)
    synopsis = models.TextField()
    votes = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField('Comments', blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    users_reactions = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True)

    def get_absolute_url(self):
        return reverse('article_detail_view', kwargs={'category_slug': self.category.slug, 'slug': self.slug})

    def __str__(self):
        return "{0}_({1})".format(str(self.slug), self.category)


class Comments(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "Comments's"

    def __str__(self):
        return str(self.id)


class UserAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    favourite_articles = models.ManyToManyField(Article, blank=True)

    def get_absolute_url(self):
        return reverse('account_view', kwargs={'user': self.user.username})

    def __str__(self):
        return self.user.username
