from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from planner.models import TaskType


class TaskTypeListView(generic.ListView):
    model = TaskType
    paginate_by = 10


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")
