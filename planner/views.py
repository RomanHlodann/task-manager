from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from planner.forms import (
    WorkerCreationForm,
    TaskCreationForm,
    TaskSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerSearchForm,
    SearchUserTaskForm,
    WorkerUpdateForm
)
from planner.models import TaskType, Worker, Task, Position


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "planner/index.html")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
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


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("planner:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
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


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("planner:worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("planner:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("planner:worker-list")


@login_required
def change_to_completed_task(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.get(id=pk)
    task.is_completed = True
    task.save()
    return HttpResponseRedirect(reverse_lazy("planner:task-list"))


@login_required
def remove_assignee_from_task(request: HttpRequest, task_id: int, assignee_id: int) -> HttpResponse:
    task = Task.objects.get(id=task_id)
    assignee = Worker.objects.get(id=assignee_id)
    task.assignees.remove(assignee)
    return HttpResponseRedirect(reverse_lazy("planner:task-detail", kwargs={'pk': task_id}))


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        find_my_task = self.request.GET.get("find_my_task", False)
        today = datetime.today()
        context["today"] = today
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        context["user_task_form"] = SearchUserTaskForm(
            initial={"find_my_task": find_my_task}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        search_form = TaskSearchForm(self.request.GET)
        user_task_form = SearchUserTaskForm(self.request.GET)
        if search_form.is_valid():
            queryset = queryset.filter(name__icontains=search_form.cleaned_data["name"])
        if user_task_form.is_valid() and user_task_form.cleaned_data.get("find_my_task", False):
            t = user_task_form.cleaned_data.get("find_my_task", False)
            queryset = queryset.filter(id=self.request.user.id)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("planner:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("planner:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("planner:task-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
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


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("planner:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("planner:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("planner:position-list")
