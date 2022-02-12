from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from users.models import User


@login_required
def forest(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    if request.user == user:
        return render(request, 'forest/myforest.html', context)
    else:
        return render(request, 'forest/forest.html', context)


@login_required
def add_tree(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        user.forest.add_tree()
    return redirect('forest', user)