from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def poll(request):
    return render(request, 'pages/polls.html')