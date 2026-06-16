from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User

FIELD_ATTRS = {'class': 'form--control'}

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your password', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={**FIELD_ATTRS, 'placeholder': 'Confirm password'}))
    referral_code = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Referral code (optional)'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'referral_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
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
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'country', 'avatar']


class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'country', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={**FIELD_ATTRS, 'id': 'username'}),
            'country': forms.TextInput(attrs={**FIELD_ATTRS, 'id': 'country'}),
            'phone': forms.TextInput(attrs={**FIELD_ATTRS, 'id': 'mobile', 'placeholder': 'Your mobile number'}),
        }
