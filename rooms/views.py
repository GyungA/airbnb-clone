from django.core.paginator import EmptyPage
from django.views.generic import ListView
from django.shortcuts import redirect
from . import models

class HomeView(ListView):

    """ HomeView Definition"""
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
