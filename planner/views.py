from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from planner.forms import WorkerCreationForm, TaskCreationForm, TaskSearchForm, PositionSearchForm, TaskTypeSearchForm, \
    WorkerSearchForm
from planner.models import TaskType, Worker, Task, Position


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "<h1>Home</h1>")


class TaskTypeListView(generic.ListView):
    model = TaskType
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = "__all__"
    success_url = reverse_lazy("planner:worker-detail")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("planner:worker-list")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        today = datetime.today()
        context["today"] = today
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("planner:task-detail")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("planner:task-detail")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("planner:task-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("planner:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("planner:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("planner:position-list")
