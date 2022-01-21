from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def writingEnv(request):
    return render(request, 'writing_env/writingEnv.html')



