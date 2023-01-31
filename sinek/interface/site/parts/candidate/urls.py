from django.urls import path
from django.views.generic.base import RedirectView

from .views import (AnchorTestView, ComplexTestView, DashboardView,
                    DiscSuccessView, DiscTestView, Tmms24TestView)

app_name = 'candidate'

urlpatterns = [
  path('', RedirectView.as_view(url='dashboard/')),
  path('dashboard/', DashboardView.as_view(), name='dashboard'),
  path('test/1/', DiscTestView.as_view(), name='disc'),
  path('test/2/', Tmms24TestView.as_view(), name='tmms24'),
  path('test/3/', AnchorTestView.as_view(), name='anchor'),
  path('test/4/', ComplexTestView.as_view(), name='complex'),
  path('test/success/', DiscSuccessView.as_view(), name='disc-success'),
]
