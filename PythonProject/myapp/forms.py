from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Listing

User = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class UploadPhotoListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['image']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Введите действующий email адрес.')
    first_name = forms.CharField(max_length=30, help_text='Введите ваше имя.')
    last_name = forms.CharField(max_length=30, help_text='Введите вашу фамилию.')
    phone = forms.CharField(max_length=15, help_text='Введите ваш телефон.')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")


        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")


        if len(password1) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну букву.")

        return password2
class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        required=True
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Неверный email или пароль.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'location', 'image']


from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Введите сообщение...'
            })
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'avatar']
