from django.urls import path

from planner.views import (
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView
)


urlpatterns = [
    path('task-type/', TaskTypeListView.as_view(), name="task-type-list"),
    path('task-type/create', TaskTypeCreateView.as_view(), name="task-type-create"),
    path('task-type/<int:pk>/update', TaskTypeUpdateView.as_view(), name="task-type-update"),
    path('task-type/<int:pk>/delete', TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path('worker/', WorkerListView.as_view(), name="worker-list"),
    path('worker/create', WorkerCreateView.as_view(), name="worker-create"),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name="worker-detail"),
    path('worker/<int:pk>/update', WorkerUpdateView.as_view(), name="worker-update"),
    path('worker/<int:pk>/delete', WorkerDeleteView.as_view(), name="worker-delete"),
]

app_name = "planner"
