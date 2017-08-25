from django.shortcuts import render, HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.
def createUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        userForm = UserForm(request.POST)
        # check whether it's valid:
        if userForm.is_valid():
            new_user = User.objects.create_user(**userForm.cleaned_data)
            # login(new_user)
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        userForm = UserForm()

    return render(request, 'registration/createUser.html', context={"form":userForm})
