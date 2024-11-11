from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.http import request
from django_select2.forms import Select2Widget
from .models import Priorities, Task, Assignee, Status, Todo


class TaskForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, label="Clear current image")

    class Meta:
        model = Task
        fields = ['title', 'description', 'hours', 'assigned_to', 'status', 'priority', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'hours': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': Select2Widget(attrs={'class': 'form-control'}),  # Using Select2Widget
            'status': Select2Widget(attrs={'class': 'form-control'}),  # Using Select2Widget
            'priority': Select2Widget(attrs={'class': 'form-control'}),  # Using Select2Widget
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        task = super().save(*args, **kwargs)  # Save the task instance first
        if self.cleaned_data.get('clear_image'):
            if task.image:  # Check if there's an image to delete
                task.image.delete(save=True)  # Delete the image file from storage
        return task

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Initialize form helper for crispy-forms
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save Task'))

        # Handle custom queryset for status and priority fields
        self.fields['status'].queryset = Status.objects.all()
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

        self.fields['priority'].queryset = Priorities.objects.all()  # Make sure Priority is a different model
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})

        # Optionally, set a class for the clear_image checkbox
        self.fields['clear_image'].widget.attrs.update({'class': 'form-check-input'})


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