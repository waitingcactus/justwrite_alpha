from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import User

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

