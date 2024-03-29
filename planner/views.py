from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from planner.forms import WorkerCreationForm
from planner.models import TaskType, Worker


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


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 10


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    success_url = reverse_lazy("planner:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("planner:worker-list")
