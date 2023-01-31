from django.test import TestCase

from sinek.domain.model.freelancer import ConditionBuilder, Initial, Talent, FullTime, HalfTime, Lancer


class ConditionBuilderTestCase(TestCase):
  kAsTalentArgs = (
    (50.5, 51.5),
    Talent.Disponibility.ONEMONTH,
    Talent.Modality.HYBRID,
    'Mi dreamjob')
  kAsHalfTimeArgs = (5, HalfTime.Experience.HIGH)

  def setUp(self) -> None:
    self.conditionBuilder = ConditionBuilder()

  def test_empty(self):
    self.assertRaises(ValueError, lambda: self.conditionBuilder.Build())

  def test_initial(self):
    condition = self.conditionBuilder.AsInitial().Build()
    self.assertIsInstance(condition, Initial)

  def test_talent(self):
    condition = self.conditionBuilder.AsTalent(*self.kAsTalentArgs).Build()
    self.assertIsInstance(condition, Talent)

  def test_halftime(self):
    condition = self.conditionBuilder.AsHalfTime(*self.kAsHalfTimeArgs).Build()
    self.assertIsInstance(condition, HalfTime)

  def test_fulltime(self):
    condition = self.conditionBuilder.AsFullTime().Build()
    self.assertIsInstance(condition, FullTime)

  def test_only_one_pre_initial_talent(self):
    self.conditionBuilder.AsInitial()
    self.assertRaises(
      TypeError,
      lambda: self.conditionBuilder.AsTalent(
        *self.kAsTalentArgs))

  def test_only_one_pre_initial_halftime(self):
    self.conditionBuilder.AsInitial()
    self.assertRaises(
      TypeError,
      lambda: self.conditionBuilder.AsHalfTime(
        *self.kAsHalfTimeArgs))

  def test_only_one_pre_initial_fulltime(self):
    self.conditionBuilder.AsInitial()
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsFullTime())

  def test_only_one_post_initial_talent(self):
    self.conditionBuilder.AsTalent(*self.kAsTalentArgs)
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsInitial())

  def test_only_one_post_initial_halftime(self):
    self.conditionBuilder.AsHalfTime(*self.kAsHalfTimeArgs)
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsInitial())

  def test_only_one_post_initial_fulltime(self):
    self.conditionBuilder.AsFullTime()
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsInitial())

  def test_double_initial(self):
    self.conditionBuilder.AsInitial()
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsInitial())

  def test_mix_talent_fulltime(self):
    condition = self.conditionBuilder.AsTalent(
      *self.kAsTalentArgs).AsFullTime().Build()
    self.assertIsInstance(condition, Talent)
    self.assertIsInstance(condition, FullTime)
    self.assertIsInstance(condition, Lancer)

  def test_mix_fulltime_talent(self):
    condition = self.conditionBuilder.AsFullTime().AsTalent(*self.kAsTalentArgs).Build()
    self.assertIsInstance(condition, Talent)
    self.assertIsInstance(condition, FullTime)
    self.assertIsInstance(condition, Lancer)

  def test_mix_talent_halftime(self):
    condition = self.conditionBuilder.AsHalfTime(
      *self.kAsHalfTimeArgs).AsTalent(*self.kAsTalentArgs).Build()
    self.assertIsInstance(condition, Talent)
    self.assertIsInstance(condition, HalfTime)
    self.assertIsInstance(condition, Lancer)

  def test_mix_halftime_talent(self):
    condition = self.conditionBuilder.AsTalent(
      *
      self.kAsTalentArgs).AsHalfTime(
      *
      self.kAsHalfTimeArgs).Build()
    self.assertIsInstance(condition, Talent)
    self.assertIsInstance(condition, HalfTime)
    self.assertIsInstance(condition, Lancer)

  def test_not_allowed_halftime_fulltime(self):
    self.conditionBuilder.AsHalfTime(*self.kAsHalfTimeArgs)
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsFullTime())

  def test_not_allowed_fulltime_halftime(self):
    self.conditionBuilder.AsFullTime()
    self.assertRaises(
      TypeError,
      lambda: self.conditionBuilder.AsHalfTime(
        *self.kAsHalfTimeArgs))

  def test_not_allowed_double_talent(self):
    self.conditionBuilder.AsTalent(*self.kAsTalentArgs)
    self.assertRaises(
      TypeError,
      lambda: self.conditionBuilder.AsTalent(
        *self.kAsTalentArgs))

  def test_not_allowed_double_halftime(self):
    self.conditionBuilder.AsHalfTime(*self.kAsHalfTimeArgs)
    self.assertRaises(
      TypeError,
      lambda: self.conditionBuilder.AsHalfTime(
        *self.kAsHalfTimeArgs))

  def test_not_allowed_double_fulltime(self):
    self.conditionBuilder.AsFullTime()
    self.assertRaises(TypeError, lambda: self.conditionBuilder.AsFullTime())
