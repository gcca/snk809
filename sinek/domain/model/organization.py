from neom.ddd.shared import Entity, Identity


class OrganizationId(Identity):
  id_: int


class Organization(Entity):
  organizationId: OrganizationId
  name: str
