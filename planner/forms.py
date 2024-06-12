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


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name",
                  "email", "position"]


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


class TaskSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="")


class SearchUserTaskForm(forms.Form):
    find_my_task = forms.BooleanField(label=False, required=False)


class PositionSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="")


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="")


class WorkerSearchForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, label="")
