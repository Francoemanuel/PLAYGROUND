
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from datetime import date

def home(request):
    today = date.today()
    stack = [
            {'id': 'python', 'name': 'Python'},
            {'id': 'django', 'name': 'Django'},
            {'id': 'php', 'name': 'PHP'},
            {'id': 'golang', 'name': 'Golang'},
            {'id': 'js', 'name': 'JS'}
        ]
    return render(request, "landing/landing.html", {
        "name": "Franco",
        "today": today,
        "age": 33,
        "stack": stack
    })
    
    
def stack_detail(request, tool):

    return HttpResponse(f"Tecnología: {tool}")
