# =============================================================================
# Copyright Snk809, Inc. All rights reserved.
# =============================================================================

from django import urls
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from . import models


class DashboardView(TemplateView):
    template_name = "customers/dashboard.html"


class ListView(ListView):
    template_name = "customers/list.html"
    model = models.Customer


class CreateView(CreateView):
    template_name = "customers/form.html"
    success_url = urls.reverse_lazy("customers:list")
    model = models.Customer
    fields = "__all__"


class DetailView(DetailView):
    template_name = "customers/detail.html"
    model = models.Customer
    pk_url_kwarg = "customer_id"


class UpdateView(UpdateView):
    template_name = "customers/form.html"
    success_url = urls.reverse_lazy("customers:list")
    model = models.Customer
    fields = "__all__"
    pk_url_kwarg = "customer_id"
