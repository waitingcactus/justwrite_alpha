from django.utils import timezone
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import token_generator

from .models import User
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm


def send_verification_email(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_active:
        return redirect('profile', username)

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    template = render_to_string('users/email_templates/verification_email.html',
                                {'username': user.username,
                                 'domain': get_current_site(request).domain,
                                 'uidb64': uidb64,
                                 'token': token_generator.make_token(user)})
    email = EmailMessage(
        'Verify email',
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.fail_silently = False
    email.send()
    return redirect('email-sent', user)


def email_sent(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'users/verification_email_sent.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            return redirect('login')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account successfully activated!')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid.')
        return redirect('landing')


def register(request):
    if request.method == 'POST':
        u_form = RegistrationForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            user = User.objects.get(username=username)
            send_verification_email(request, user)
            return redirect('email-sent', username)
    else:
        u_form = RegistrationForm()
    return render(request, 'users/register.html', {'u_form': u_form})


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
            u_form = UserUpdateForm(request.POST, instance=user) #instantiate forms with updated info
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
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
