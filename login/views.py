from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm


def login_user(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def login_submit(request):
    form = AuthenticationForm(data=request.POST)
    if form is not None and form.is_valid():
        user = authenticate(request, username=form.cleaned_data.get('username'), 
                            password=form.cleaned_data.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return login_submission_failure(request, {'form': form}) 
    else:
        return login_submission_failure(request, {'form': form}) 


def new_user(request):
    new_user_form = NewUserForm()
    return render(request, 'new_user.html', {'form': new_user_form})


def new_user_submit(request):
    new_user_form = NewUserForm(data=request.POST)
    if new_user_form is not None and new_user_form.is_valid():
        new_user_form.save()
        user = authenticate(request, username=new_user_form.cleaned_data.get('username'), 
                            password=new_user_form.cleaned_data.get('password1'))
        if user is not None:
            login(request, user)
            return redirect('/user-preferences/' + str(user.id) +
                            '/')
        else:
            return new_user_submission_failure(request, {'form': new_user_form})
    else:
        return new_user_submission_failure(request, {'form': new_user_form})


def login_submission_failure(request, context):
    context['failure'] = True
    return render(request, 'login.html', context)


def new_user_submission_failure(request, context=None):
    return render(request, 'new_user.html', context)


def register_preferences(request):
    pass
