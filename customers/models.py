# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=256)
