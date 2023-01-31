from django import forms


class NewFreelancerForm(forms.Form):
  name = forms.CharField(max_length=128)
  username = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64, widget=forms.PasswordInput)

  username.widget.attrs.update(autofocus='on')
