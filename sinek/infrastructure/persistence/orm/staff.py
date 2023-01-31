from sinek.domain.model.staff import Staff, StaffRepository

from .models import Staff as ORMStaff


class StaffRepositoryORM(StaffRepository):

  def Store(self, staff: Staff):
    try:
      ormStaff = ORMStaff.objects.get(
        name=staff.name)
    except ORMStaff.DoesNotExist:
      ormStaff = ORMStaff()

    ormStaff.name = staff.name

    ormStaff.save()
