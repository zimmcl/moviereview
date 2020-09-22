from django import forms
from moviereview_app.models import Article, Category
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
        self.fields['username'].label = ''
        self.fields['password'].label = ''

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
        widget=forms.PasswordInput, label='Repeat password')
    email = forms.CharField(widget=forms.EmailInput,
                            help_text='Please, provide real email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['password_check'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "User with this username already exists.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        if password != password_check:
            raise forms.ValidationError("Passwords dont match.")


class CategoryCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nombre'}))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ''}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Descripcion completa'}))

    def __init__(self, *args, **kwargs):
        super(CategoryCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['slug'].label = ''
        self.fields['description'].label = ''

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
        self.fields['title'].label = ''
        self.fields['slug'].label = ''
        self.fields['synopsis'].label = ''
        self.fields['category'].label = ''
        self.fields['image'].label = ''
        self.fields['url_embed'].label = ''

    class Meta:
        model = Article
        fields = ('title', 'slug', 'image',
                  'category', 'synopsis', 'url_embed')


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
