from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150)
    referral_code = forms.CharField(max_length=20, required=False, label='Referral Code (optional)')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'referral_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        ref_code = self.cleaned_data.get('referral_code')
        if ref_code:
            try:
                referrer = User.objects.get(referral_code=ref_code)
                user.referred_by = referrer
            except User.DoesNotExist:
                pass
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'country', 'avatar']


class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'country', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form--control', 'id': 'username'}),
            'country': forms.TextInput(attrs={'class': 'form-control form--control', 'id': 'country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form--control', 'id': 'mobile'}),
        }
