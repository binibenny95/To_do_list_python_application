from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.http import request
from django_select2.forms import Select2Widget
from .models import Task, Assignee, Status, Todo


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'hours', 'assigned_to', 'status', 'priority']
        widgets = {
            'assigned_to': Select2Widget(attrs={'class': 'form-control'}),
            'status': Select2Widget(attrs={'class': 'form-control'}),
            'priority': Select2Widget(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)  # Remove 'user' from kwargs
            super(TaskForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'POST'
            self.helper.add_input(Submit('submit', 'Save Task'))

            # Many to One, form basic select
            self.fields['status'].queryset = Status.objects.all()
            self.fields['status'].widget.attrs.update({'class': 'form-control'})

            # Many to One, form basic select
            self.fields['priority'].queryset = Status.objects.all()
            self.fields['priority'].widget.attrs.update({'class': 'form-control'})


class AssigneeForm(forms.ModelForm):
    class Meta:
        model = Assignee
        fields = ['name', 'email']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'POST'
            self.helper.add_input(Submit('submit', 'Save Assignee'))


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a new todo...'}),
        }
