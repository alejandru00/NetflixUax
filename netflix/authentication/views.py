from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)