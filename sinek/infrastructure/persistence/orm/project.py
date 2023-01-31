from typing import List


from sinek.domain.model.project import Project, ProjectRepository

from .models import Project as ORMProject


class ProjectRepositoryORM(ProjectRepository):

  def All(self) -> List[Project]:
    ormProjects = ORMProject.objects.all()
    projects = [self._makeFrom(project)
                for project in ormProjects]
    return projects

  def _makeFrom(self, ormProject: ORMProject) -> Project:
    return Project(
      name=ormProject.name
    )

  # TODO: Agregar logica para incluir account manager
  def Store(self, project: Project):
    try:
      ormProject = ORMProject.objects.get(name=project.name)
    except ORMProject.DoesNotExist:
      #User = get_user_model()
      # user = User.objects.create_user(
      #  username=accountManager.name, password=accountManager.name)
      ormProject = ORMProject()

    ormProject.name = project.name
    ormProject.save()
