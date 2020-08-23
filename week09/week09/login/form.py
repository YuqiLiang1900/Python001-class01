from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

