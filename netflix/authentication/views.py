from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

# Vista de registro
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguear automáticamente al registrarse
            messages.success(request, "Account created successfully!")
            return redirect('/')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('/login/')
