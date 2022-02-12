from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages

from .forms import ProjectForm
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


def create_project(request, username):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        user = User.objects.get(username=username)
        form.instance.user = user
        if form.is_valid():
            form.save()
            return redirect('projects', request.user)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        project = Project.objects.get(id=pk)
        return super(ProjectDetailView, self).get_context_data()


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['name', 'file']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Project successfully created.')
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.user:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project

    def get_success_url(self):
        return reverse('projects', kwargs={'username': self.request.user})

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.user:
            return True
        return False
