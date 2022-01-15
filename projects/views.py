from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib import messages

from users.models import User
from .models import Project

@login_required
def projects(request, username):
    """
    Displays projects of requested user if
    user is authenticated.
    """
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    if request.user.is_authenticated and request.user == user:  # logged-in user == requested user
        return render(request, 'projects/myprojects.html', context)
    else:  # return view-only profile page
        return render(request, 'projects/projects.html', context)


class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'file']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Project successfully created.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error.')
        return super().form_invalid(form)

