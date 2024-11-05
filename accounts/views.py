from django.contrib.auth import login as auth_login, logout as auth_logout  # Rename the imported functions
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Call the imported login function
            return redirect('tasks:home_menu')  # Redirect to your home page or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Call the imported login function
            return redirect('tasks:home_menu')  # Redirect to home page or another page
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Logout view
def logout_view(request):
    auth_logout(request)  # Call the imported logout function
    return redirect('login')  # Redirect to login page after logout
