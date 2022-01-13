from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm

def home(request):
    return render(request, 'users/home.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username):
    """
    Displays myprofile.html if logged-in user == requested user,
    else displays profile.html.
    """
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    if request.user.is_authenticated and request.user == user: #logged-in user == requested user
        if request.method == 'POST': #form submit button has been pressed
            u_form = UserUpdateForm(request.POST, instance=request.user) #instantiate forms with updated info
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid(): #info entered is valid
                user.last_name_change = timezone.now()
                u_form.save()
                p_form.save()
                messages.success(request, 'Changes saved.')

                return redirect('profile', u_form.instance) #u_form.instance returns updated username

        else:
            u_form = UserUpdateForm(instance=request.user) #fills forms with logged-in user's info
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context['u_form'] = u_form
        context['p_form'] = p_form
        return render(request, 'users/myprofile.html', context)
    else: #return view-only profile page
        return render(request, 'users/profile.html', context)
