from django.shortcuts import render, get_object_or_404, redirect

from users.models import User


def forest(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'forest/forest.html', context)


def add_tree(request, username):
    user = get_object_or_404(User, username=username)
    user.forest.add_tree()
    return redirect('forest', user)