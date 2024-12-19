from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from .models import CustomUser, ResetPassword, NewPassword


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Никнейм",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"}),
    )
    email = forms.EmailField(
        label="Электронная почта", widget=forms.EmailInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "style": "width: 400px"})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class CustomUserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label="Никнейм",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"}),
    )
    email = forms.EmailField(
        label="Электронная почта", widget=forms.EmailInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    phone_number = forms.IntegerField(
        label="Телефонный номер",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "style": "width: 400px"}),
    )
    avatar = forms.FileField(
        label="Фотография профиля",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "style": "width: 400px"}),
    )
    country = forms.CharField(
        label="Страна",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"}),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "avatar", "country")


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Электронная почта", widget=forms.EmailInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    password = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "style": "width: 400px"})
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = ResetPassword
        fields = ("email",)


class NewPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        label="Электронная почта", widget=forms.EmailInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label="Подтверждение нового пароля", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = NewPassword
        fields = ("email", "password1", "password2")