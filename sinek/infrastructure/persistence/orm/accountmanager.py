from sinek.domain.model.accountmanager import (AccountManager,
                                               AccountManagerRepository)

from .models import AccountManager as ORMAccountManager


class AccountManagerRepositoryORM(AccountManagerRepository):

  def Store(self, accountManager: AccountManager):
    try:
      ormAccountManager = ORMAccountManager.objects.get(
        email=str(accountManager.email))
    except ORMAccountManager.DoesNotExist:
      ormAccountManager = ORMAccountManager()

    ormAccountManager.name = accountManager.name
    ormAccountManager.email = str(accountManager.email)

    ormAccountManager.save()
