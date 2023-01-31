from django import forms


class NewHunterForm(forms.Form):
  username = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64, widget=forms.PasswordInput)
  name = forms.CharField(max_length=128)

  username.widget.attrs.update(autofocus='on')


class NewAccountManagerForm(forms.Form):
  email = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64, widget=forms.PasswordInput)
  name = forms.CharField(max_length=128)

  email.widget.attrs.update(autofocus='on')
