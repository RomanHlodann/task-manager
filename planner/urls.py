from django.urls import path

from planner.views import (
    index,
    change_to_completed_task,
    remove_assignee_from_task,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView
)


urlpatterns = [
    path("", index, name="index"),
    path("task-type/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-type/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-type/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/change_to_completed", change_to_completed_task, name="task-change-to-completed"),
    path("task/<int:task_id>/remove/<int:assignee_id>", remove_assignee_from_task, name="task-remove-assignee"),
    path("position/", PositionListView.as_view(), name="position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
]

app_name = "planner"
