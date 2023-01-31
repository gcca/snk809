from django import forms

from sinek.domain.model.freelancer import Network, Phone


class PersonalForm(forms.Form):
  CHOICES = (
    (Phone.CountryCode.ARG.name, 'ARG'),
    (Phone.CountryCode.BOL.name, 'BOL'),
    (Phone.CountryCode.BRA.name, 'BRA'),
    (Phone.CountryCode.CHI.name, 'CHI'),
    (Phone.CountryCode.COL.name, 'COL'),
    (Phone.CountryCode.CRI.name, 'CRI'),
    (Phone.CountryCode.CUB.name, 'CUB'),
    (Phone.CountryCode.ECU.name, 'ECU'),
    (Phone.CountryCode.SLV.name, 'SLV'),
    (Phone.CountryCode.GTM.name, 'GTM'),
    (Phone.CountryCode.HTI.name, 'HTI'),
    (Phone.CountryCode.HND.name, 'HND'),
    (Phone.CountryCode.MEX.name, 'MEX'),
    (Phone.CountryCode.NIC.name, 'NIC'),
    (Phone.CountryCode.PAN.name, 'PAN'),
    (Phone.CountryCode.PRY.name, 'PRY'),
    (Phone.CountryCode.PER.name, 'PER'),
    (Phone.CountryCode.URY.name, 'URY'),
    (Phone.CountryCode.VEN.name, 'VEN'),
  )

  CHOICES_COUNTRY = (
    ('Argentina', 'Argentina'),
    ('Bolivia', 'Bolivia'),
    ('Brasil', 'Brasil'),
    ('Chile', 'Chile'),
    ('Colombia', 'Colombia'),
    ('Costa Rica', 'Costa Rica'),
    ('Cuba', 'Cuba'),
    ('Ecuador', 'Ecuador'),
    ('Salvador', 'Salvador'),
    ('Guatemala', 'Guatemala'),
    ('Haití', 'Haití'),
    ('Honduras', 'Honduras'),
    ('México', 'México'),
    ('Nicaragua', 'Nicaragua'),
    ('Panamá', 'Panamá'),
    ('Paraguay', 'Paraguay'),
    ('Perú', 'Perú'),
    ('Uruguay', 'Uruguay'),
    ('Venezuela', 'Venezuela'),
  )

  name = forms.CharField(max_length=128)
  phoneCountryCode = forms.ChoiceField(
    choices=CHOICES,
    widget=forms.Select(attrs={'class': 'country-code'}))
  countryCode = forms.ChoiceField(
    choices=CHOICES_COUNTRY,
    widget=forms.Select())
  phone = forms.CharField(max_length=64)
  location = forms.CharField(max_length=128)
  country = forms.CharField(max_length=128)
  condition = forms.CharField()


class NetworkForm(forms.Form):
  CHOICES = (
    (Network.Kind.GITHUB.value, 'Github'),
    (Network.Kind.LINKEDIN.value, 'Linkedin'),
    (Network.Kind.BEHANCE.value, 'Behance')
  )

  network = forms.ChoiceField(
    choices=CHOICES,
    widget=forms.Select(
      attrs={
        'class': 'luci-complex-select'}))
  url = forms.URLField(
    max_length=256,
    widget=forms.URLInput(
      attrs={
        'class': 'luci-text-field w-100',
        'placeholder': 'Pega el link'}))


class NetworkDeleteForm(forms.Form):
  url = forms.URLField(max_length=256)


class BusinessForm(forms.Form):
  name = forms.CharField(max_length=128)


class ProjectForm(forms.Form):
  name = forms.CharField(max_length=128)


class UploadForm(forms.Form):
  upload = forms.FileField()
