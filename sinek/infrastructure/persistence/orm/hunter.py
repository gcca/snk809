
from sinek.domain.model.hunter import Hunter, HunterRepository

from .models import Hunter as ORMHunter


class HunterRepositoryORM(HunterRepository):

  def Find(self, name: str) -> Hunter:
    ormHunter = ORMHunter.objects.get(name=name)
    hunter = Hunter(name=ormHunter.name)
    return hunter

  def Store(self, hunter: Hunter):
    try:
      ormHunter = ORMHunter.objects.get(name=hunter.name)
    except ORMHunter.DoesNotExist:
      ormHunter = ORMHunter()

    ormHunter.name = hunter.name
    ormHunter.save()
