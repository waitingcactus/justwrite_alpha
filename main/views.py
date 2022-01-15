from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'main/home.html', {'user': request.user})


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/landing.html')
