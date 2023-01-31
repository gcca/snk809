from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from neom.core.ioc import AutoWire


@AutoWire
class SampleDataTestCase(TestCase):
  def test_permission_creation(self):
    content_type = ContentType.objects.get_for_model(User)
    permissions = [
      Permission(codename='im_hunter',
                 name='Can access Hunter views',
                 content_type=content_type),
      Permission(codename='im_candidate',
                 name='Can access Candidate views',
                 content_type=content_type),
      Permission(codename='im_accountmanager',
                 name='Can access Account Manager views',
                 content_type=content_type),
      Permission(codename='im_freelancer',
                 name='Can access Freelancer views',
                 content_type=content_type),
      Permission(codename='im_staff',
                 name='Can access Staff views',
                 content_type=content_type),
    ]

    for permission in permissions:
      Permission.objects.get(codename=permission.codename,
                             name=permission.name,
                             content_type=permission.content_type)
