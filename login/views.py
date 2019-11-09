from enum import Enum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
#from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password 
from .new_user_validator import NewUserValidator, NewUserSubmissionErrors
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import NewUserForm

def login_user(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def login_submit(request):
    form = AuthenticationForm(request)
    if form is not None and form.is_valid():
        user = authenticate(request, username=form.cleaned_data.get('username'), 
                            password=form.cleaned_data.get('password'))
        if user is not None:
            login(request, user)
            redirect('/home/')
        else:
            return login_submission_failure(request, {'form': form}) 
    else:
        return login_submission_failure(request, {'form': form}) 

#def submit(request):
#    email = request.POST.get('email')
#    password = request.POST.get('password')
#    if email is None or password is None:
#        return login_submission_failure(request)
#
#    user = None
#    try:
#        user = User.objects.get(email=email)
#    except User.DoesNotExist:
#        pass
#    if user is None:
#        return login_submission_failure(request)
#    
#    hashed_pass = user.hashed_password
#
#    correct_password = check_password(password, hashed_pass)
#    if not correct_password:
#        return login_submission_failure(request)
#    else:
#        return redirect('/home/')

def new_user(request):
    new_user_form = NewUserForm()
    return render(request, 'new_user.html', {'form': new_user_form})

def new_user_submit(request):
    new_user_form = NewUserForm(request.POST)
    if new_user_form is not None and new_user_form.is_valid():
        new_user_form.save()
        user = authenticate(request, username=new_user_form.cleaned_data.get('username'), 
                            password=new_user_form.cleaned_data.get('password1'))
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return new_user_submission_failure(request, {'form': new_user_form})
    else:
        return new_user_submission_failure(request, {'form': new_user_form})

#def new_user_submit(request):
#    context = {}
#
#    name = request.POST.get('name')
#    email = request.POST.get('email')
#    password = request.POST.get('password')
#    new_user_validator = NewUserValidator(name, email, password)
#    invalid_field = False 
#
#    if new_user_validator.missing_fields:
#        if new_user_validator.missing_email:
#            context[NewUserSubmissionErrors.MISSING_EMAIL.value] = True
#        if new_user_validator.missing_name:
#            context[NewUserSubmissionErrors.MISSING_NAME.value] = True
#        if new_user_validator.missing_password:
#            context[NewUserSubmissionErrors.MISSING_PASSWORD.value] = True
#        
#        return new_user_submission_failure(request, context)
#    
#    if new_user_validator.invalid_name:
#        context[NewUserSubmissionErrors.INVALID_NAME.value] = True
#        invalid_field = True
#
#    if new_user_validator.invalid_email:
#        context[NewUserSubmissionErrors.INVALID_EMAIL.value] = True
#        invalid_field = True
#    
#    if new_user_validator.overshort_password:
#        context[NewUserSubmissionErrors.OVERSHORT_PASSWORD.value] = True
#        invalid_field = True
#    
#    if new_user_validator.duplicate_email:
#        context[NewUserSubmissionErrors.DUPLICATE_EMAIL.value] = True
#        invalid_field = True
#
#    if invalid_field:
#        return new_user_submission_failure(request, context)
#
#    else:
#        User.create_user(email, password, name)
#        return redirect('/home/')
   

def login_submission_failure(request, context):
    context = {'failure': True}
    return render(request, 'login.html', context)

def new_user_submission_failure(request, context=None):
    return render(request, 'new_user.html', context)

def register_preferences(request):
    pass
    