from django import forms


class UserAuthenticate(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
