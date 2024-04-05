from django.shortcuts import render

# Create your views here.


def Dash(request):
    return render(request , "index.html")