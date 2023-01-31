from django.test import TestCase

from neom.core.ioc import AutoWire

from sinek.domain.model.freelancer import Knowledge
from sinek.domain.model.skill import Skill
from sinek.domain.service import AutoKnowledgeService


@AutoWire
class AutoSkillsTestCase(TestCase):

  autoKnowledgeService: AutoKnowledgeService

  kNotScoredSkills = {Skill(1, 'AWS'), Skill(2, 'MySQL'),
                      Skill(3, 'MySQL'), Skill(1, 'AWS'),
                      Skill(4, 'Java 6'), Skill(5, 'Java 8'),
                      Skill(6, 'React JS'), Skill(7, 'Preact')}

  def test_match_not_exact_knowledges(self):
    skillName = 'React.JS'

    matches = self.autoKnowledgeService._getCloseMatches(
      skillName, self.kNotScoredSkills, 50)

    react1 = Skill(6, 'React JS')
    react2 = Skill(7, 'Preact')

    self.assertEqual(len(matches), 2)
    self.assertIn(react1, matches)
    self.assertIn(react2, matches)

  def test_match_inclusive_string_knowledges(self):
    skillName = 'Java'
    matches = self.autoKnowledgeService._getCloseMatches(
      skillName, self.kNotScoredSkills)

    java1 = Skill(4, 'Java 6')
    java2 = Skill(5, 'Java 8')

    self.assertIn(java1, matches)
    self.assertIn(java2, matches)
    self.assertEqual(len(matches), 2)
