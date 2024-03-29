from django.urls import path

from planner.views import (
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView
)


urlpatterns = [
    path('task-type/', TaskTypeListView.as_view(), name="task-type-list"),
    path('task-type/create', TaskTypeCreateView.as_view(), name="task-type-create"),
    path('task-type/<int:pk>/update', TaskTypeUpdateView.as_view(), name="task-type-update"),
    path('task-type/<int:pk>/delete', TaskTypeDeleteView.as_view(), name="task-type-delete"),
]
