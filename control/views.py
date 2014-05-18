from django.shortcuts import render

# Create your views here.
def control(request):
    return render(request, "control.html")
    