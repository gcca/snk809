from typing import List, Tuple, cast

from neom.core.ioc import AutoWire

from sinek.infrastructure.persistence.orm import Freelancer
from sinek.domain.model.freelancer import (Email, FreelancerQueryService,
                                           FreelancerRepository)
from sinek.domain.model.skill import SkillQueryService
from sinek.domain.service import FreelancerKnowledgeTreeService, ProfileService
from sinek.interface.site.parts.freelancer.adapter import ProfileViewAdapter


@AutoWire
class ProfileServiceFacade:

  freelancerRepository: FreelancerRepository
  freelancerQueryService: FreelancerQueryService
  freelancerKnowledgeTreeService: FreelancerKnowledgeTreeService
  profileService: ProfileService
  skillQueryService: SkillQueryService

  def Load(self, email: Email) -> ProfileViewAdapter:

    businesses = self.freelancerQueryService.ListAllBusinesses()
    projects = self.freelancerQueryService.ListAllProjects()
    freelancer = self.freelancerRepository.Find(email)
    cvs, files = self.profileService.GetProfile(freelancer)
    knowledges = self.freelancerQueryService.ListKnowledges(freelancer)
    skillTree = self.skillQueryService.LoadRolesKnowledgeTree(freelancer.roleInterests)
    tree = self.freelancerKnowledgeTreeService.MakeTreeEdit(
      knowledges.copy(), skillTree)
    freelancerId = Freelancer.objects.get(email=freelancer.email).id

    return ProfileViewAdapter(
      freelancer, cvs, files, knowledges), businesses, projects, tree
