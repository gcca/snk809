from django.urls import include, path
from django.views.generic.base import RedirectView

from sinek.interface.site.parts.account import urls as AccountUrls
from sinek.interface.site.parts.accountmanager import \
  urls as AccountManagerUrls
from sinek.interface.site.parts.candidate import urls as CandidateUrls
from sinek.interface.site.parts.freelancer import urls as FreelancerUrls
from sinek.interface.site.parts.hunter import urls as HunterUrls
from sinek.interface.site.parts.legal_info import urls as LegalInfoUrls
from sinek.interface.site.parts.staff import urls as StaffUrls

app_name = 'site'

urlpatterns = [
  path('', RedirectView.as_view(url='account/')),
  path('account/', include(AccountUrls)),
  path('accountmanager/', include(AccountManagerUrls)),
  path('candidate/', include(CandidateUrls)),
  path('freelancer/', include(FreelancerUrls)),
  path('hunter/', include(HunterUrls)),
  path('staff/', include(StaffUrls)),
  path('legal-info/', include(LegalInfoUrls)),
]
