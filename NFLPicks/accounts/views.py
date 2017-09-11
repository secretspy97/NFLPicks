from django.shortcuts import render, HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
def createUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        userForm = UserForm(request.POST)
        # check whether it's valid:
        if userForm.is_valid():
            new_user = User.objects.create_user(**userForm.cleaned_data)
            return render(request, 'base.html', context={"message": "Your account has been created. Click 'Login' to Proceed"})

    # if a GET (or any other method) we'll create a blank form
    else:
        userForm = UserForm()

    return render(request, 'registration/createUser.html', context={"form":userForm})

def logout_view(request):
    logout(request)
    return render(request, 'base.html', context={"message": "You have been logged off"})

def profile(request):
    return HttpResponseRedirect('/viewPicks/')