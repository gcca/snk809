from django import forms


class AffiliationForm(forms.Form):
  name = forms.CharField(
    max_length=128,
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Ingrese nombre'}))
  email = forms.EmailField(
    max_length=128,
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Ingrese e-mail'}))
  gender = forms.IntegerField()
