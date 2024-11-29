import http
from lib2to3.fixes.fix_input import context
from smtpd import usage

from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import comment
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth.decorators import login_required

from tasks.forms import AssigneeForm, SubtaskForm, TaskForm, TodoForm
from tasks.models import Assignee, Comment, Subtask, Task, Status, Todo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def home_menu(request: HttpRequest) -> HttpResponse:
    tasks_list = Task.objects.filter(user=request.user)
    paginator = Paginator(tasks_list, 10)
    page_number = request.GET.get('page')
    tasks_page = paginator.get_page(page_number)
    task_counts = Task.objects.aggregate(
        completed_tasks=Count('id',
                              filter=Q(status__id=Status.objects.get(name='Completed').id) & Q(user=request.user)),
        in_progress_tasks=Count('id',
                                filter=Q(status__id=Status.objects.get(name='In Progress').id) & Q(user=request.user)),
        on_hold_tasks=Count('id', filter=Q(status__id=Status.objects.get(name='On Hold').id) & Q(user=request.user)),
    )
    assignees_list = Assignee.objects.filter(user=request.user)
    todos = Todo.objects.filter(user=request.user)
    # Initialize the form
    form = TodoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('tasks:home_menu')

    context = {
        'tasks_page': tasks_page,
        'count': task_counts,
        'assignees_list': assignees_list,
        'form': form,
        'todos': todos
    }

    return render(request, 'tasks/home_list.html', context)


################tasks###########################


# ####create task######
@login_required
def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            send_mail(
                'Task Created',
                'thank you for creating your task!',
                'test@gmail.com',
                ['binibenny92@gmail.com']
            )
            return redirect('tasks:home_menu')

    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = Assignee.objects.filter(user=request.user)
        context = {'form': form}
        return render(request, 'tasks/task_form.html', context)


####update task based on task id######
@login_required
def edit_task(request: HttpRequest, pk: int) -> HttpResponse:
    # Get the task to edit, ensuring it belongs to the logged-in user
    task = get_object_or_404(Task, pk=pk, user=request.user)

    # Retrieve the subtasks related to this task
    subtasks = Subtask.objects.filter(task_id=task.id)

    # Handle subtask form submission
    if request.method == 'POST':
        # Handle task form submission
        form = TaskForm(request.POST, request.FILES, instance=task)
        subtask_form = SubtaskForm(request.POST)  # We assume it's for creating a new subtask

        # Check if the task form is valid
        if form.is_valid():
            form.save()  # Save the task

        # Check if the subtask form is valid and create a new subtask
        if subtask_form.is_valid():
            subtask = subtask_form.save(commit=False)
            subtask.task = task  # Associate the subtask with the current task
            subtask.save()  # Save the subtask

        # Redirect to the task list or wherever appropriate after saving
        return redirect('tasks:home_menu')

    else:
        # Initialize the forms for GET request
        form = TaskForm(instance=task)
        form.fields['assigned_to'].queryset = Assignee.objects.filter(user=request.user)
        subtask_form = SubtaskForm()  # Form for creating a new subtask

    # Render the page with the task form and subtask form
    return render(request, 'tasks/task_form.html', {
        'form': form,  # Task form
        'subtask_form': subtask_form,  # Subtask form
        'subtasks': subtasks,  # Existing subtasks for the task
    })


###delete subtask based on task id#######
@login_required
def delete_subtask(request: HttpRequest, subtask_id: int) -> HttpResponse:
    # Get the subtask instance by ID
    subtask = get_object_or_404(Subtask, pk=subtask_id)

    # Delete the subtask
    subtask.delete()

    # Redirect back to the task detail page after deletion
    return redirect('tasks:edit_task', pk=subtask.task.id)


###delete task based on task id#######
@login_required
def delete_task(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:home_menu')
    return render(request, 'tasks/task_delete_confirmation.html', {'task': task})


####genrate pdf of the task ########
@login_required
def generate_pdf(request: HttpRequest, pk: int) -> FileResponse:
    task = Task.objects.get(pk=pk, user=request.user)
    response = FileResponse(genrate_pdf_file(task), as_attachment=True, filename='task.pdf')
    return response


def genrate_pdf_file(task: Task) -> BytesIO:
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # create a pdf document
    p.drawString(100, 750, "Task")

    y = 700
    p.drawString(100, y, f"Description : {task.description}")
    p.drawString(100, y - 20, f"Assignee : {task.assigned_to}")
    p.drawString(100, y - 40, f"status :{task.status}")
    y -= 60

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


###view task#####
@login_required
def view_task(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk, user=request.user)
    comments = Comment.objects.filter(task=task)
    subtasks = Subtask.objects.filter(task=task)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        Comment.objects.create(task=task, text=comment_text)
        return redirect('tasks:view_task', pk=task.id)

    return render(request, 'tasks/task_view.html', {'task': task, 'comments': comments, 'subtasks': subtasks})


##################assignee###################################################################3

##add assignee
@login_required
def create_assignee(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AssigneeForm(request.POST)
        if form.is_valid():
            assignee = form.save(commit=False)
            assignee.user = request.user
            assignee.save()
            return redirect('tasks:create_assignee')

    else:
        form = AssigneeForm()
        context = {'form': form}
        return render(request, 'tasks/assignee_form.html', context)


@login_required
def delete_assignee(request: HttpRequest, pk: int) -> HttpResponse:
    assignee = get_object_or_404(Assignee, pk=pk, user=request.user)
    if request.method == 'POST':
        assignee.delete()
        return redirect('tasks:home_menu')
    return render(request, 'tasks/assignee_delete_confirmation.html', {'assignee': assignee})


@login_required
def edit_assignee(request: HttpRequest, pk: int) -> HttpResponse:
    assignee = get_object_or_404(Assignee, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssigneeForm(request.POST, instance=assignee)
        if form.is_valid():
            form.save()
            return redirect('tasks:home_menu')
    else:
        form = AssigneeForm(instance=assignee)
        context = {'form': form}
        return render(request, 'tasks/assignee_form.html', context)


#####todo#####


# delete Todo
@login_required
def delete_todo(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('tasks:home_menu')


# search filter
@login_required
def search_tasks(request: HttpRequest) -> HttpResponse:
    tasks = []
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    assignee = request.GET.get('assignee')

    filters = Q()
    if start_date:
        filters &= Q(date__gte=start_date)
    if end_date:
        filters &= Q(date__lte=end_date)
    if assignee:
        filters &= Q(assigned_to=assignee)

    assignees = Assignee.objects.filter(user=request.user)

    tasks = Task.objects.filter(filters)

    return render(request, 'tasks/assignee_search.html', {'tasks': tasks, 'assignees': assignees})
