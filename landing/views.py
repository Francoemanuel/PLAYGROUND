from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from datetime import date


def home(request):
    today = date.today()
    stack = [{'id': 'python', 'name': 'Python'}, {'id': 'django', 'name': 'Django'}, {
        'id': 'golang', 'name': 'Golang'}, {'id': 'php', 'name': 'PHP'}, {'id': 'js', 'name': 'JS'}]
    return render(request, "landing/landing.html", {
        "name": "Fernando",
        "today": today,
        "age": 26,
        "stack": stack
    })


def stack_detail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")
