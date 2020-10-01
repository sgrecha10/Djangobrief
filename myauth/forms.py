from django import forms


class UserAuthenticate(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        print('clean')
        if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            print('clean2')
            return super(UserRegistrationForm, self).clean()
        else:
            raise forms.ValidationError(
                "Пароли не совпадают!"
            )
