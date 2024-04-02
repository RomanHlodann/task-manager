from django import forms
from django.contrib.auth.forms import UserCreationForm

from planner.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "position"
        )


class TaskCreationForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.SelectDateWidget
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"

