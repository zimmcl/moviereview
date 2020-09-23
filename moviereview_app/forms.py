from django import forms
from moviereview_app.models import Article, Category, UserAccount
from django.contrib.auth.models import User


class CommentCreationForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Comentario')

    class Meta:
        model = Article
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentCreationForm, self).__init__(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contraseña'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "User with this username doesnt exist.")
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError("Ivalid password.")


class RegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(
        widget=forms.PasswordInput, label='Repita contraseña')
    email = forms.CharField(widget=forms.EmailInput,
                            help_text='Ingrese un dirección de correo real')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contraseña'
        self.fields['password_check'].label = 'Confirmación'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['email'].label = 'Correo electrónico'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con ese nombre.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese email.")
        if password != password_check:
            raise forms.ValidationError("Contraseña no coincide.")


class CategoryCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nombre'}))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ''}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Descripción completa'}))

    def __init__(self, *args, **kwargs):
        super(CategoryCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Categoria'
        self.fields['slug'].label = 'Slug'
        self.fields['description'].label = 'Descripción'

    class Meta:
        model = Category
        fields = "__all__"


class ArticleCreationForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Titulo'}))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ''}))
    synopsis = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Descripcion completa'}))

    def __init__(self, *args, **kwargs):
        super(ArticleCreationForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Titulo'
        self.fields['slug'].label = 'Slug'
        self.fields['synopsis'].label = 'Sinopsis'
        self.fields['category'].label = 'Categoria'
        self.fields['image'].label = 'Imagen'
        self.fields['url_embed'].label = 'Url'

    class Meta:
        model = Article
        fields = ('title', 'slug', 'image',
                  'category', 'synopsis', 'url_embed')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'is_superuser')

    def save(self, user=None):
        user_profile = super(UserUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['is_staff'].label = 'Estado de membresía'
        self.fields['is_active'].label = 'Activo/Inactivo'
        self.fields['is_superuser'].label = 'Admin/User'


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Categoria'
        self.fields['slug'].label = 'Slug'
        self.fields['description'].label = 'Descripción'


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'slug', 'image',
                  'category', 'synopsis', 'url_embed')

    def __init__(self, *args, **kwargs):
        super(ArticleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Titulo'
        self.fields['slug'].label = 'Slug'
        self.fields['synopsis'].label = 'Sinopsis'
        self.fields['category'].label = 'Categoria'
        self.fields['image'].label = 'Imagen'
        self.fields['url_embed'].label = 'Url'
