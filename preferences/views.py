from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def user_preferences(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method == "POST":
        pass
    else:
       return render(request, 'user_preferences.html')
