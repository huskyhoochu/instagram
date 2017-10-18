from django import forms


class SignupForm(forms.Form):
    id = forms.CharField()
    password = forms.CharField()