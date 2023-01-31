from django.urls import include, path

from sinek.interface.rc.freelancer import urls as FreelancerUrls
from sinek.interface.rc.hunter import urls as HunterUrls

app_name = 'rc'

urlpatterns = [
  path('freelancer/', include(FreelancerUrls)),
  path('hunter/', include(HunterUrls))
]
