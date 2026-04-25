import secrets
import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect, render

from core.auth.service import AuthService
from core.forms import LoginForm, RegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        service = AuthService('password')
        result = service.authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        if result.success:
            return redirect(settings.LOGIN_REDIRECT_URL)
        error = result.error

    return render(request, 'auth/login.html', {'form': form, 'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = RegisterForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        service = AuthService('password')
        result = service.register(
            request,
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            display_name=form.cleaned_data['display_name'],
        )
        if result.success:
            return redirect(settings.LOGIN_REDIRECT_URL)
        error = result.error

    return render(request, 'auth/register.html', {'form': form, 'error': error})


def logout_view(request):
    django_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def google_redirect_view(request):
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state

    params = urllib.parse.urlencode({
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline',
        'prompt': 'select_account',
    })
    return redirect(f'https://accounts.google.com/o/oauth2/v2/auth?{params}')


def google_callback_view(request):
    # CSRF / state validation
    state = request.GET.get('state')
    if not state or state != request.session.pop('oauth_state', None):
        return render(request, 'auth/login.html', {
            'error': 'Invalid OAuth state. Please try again.',
            'form': LoginForm(),
        })

    code = request.GET.get('code')
    if not code:
        return render(request, 'auth/login.html', {
            'error': 'Authorization code missing.',
            'form': LoginForm(),
        })

    # Exchange code for tokens
    token_response = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        },
        timeout=10,
    )

    if token_response.status_code != 200:
        return render(request, 'auth/login.html', {
            'error': 'Failed to obtain access token from Google.',
            'form': LoginForm(),
        })

    token_data = token_response.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token', '')

    # Fetch user info
    userinfo_response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=10,
    )

    if userinfo_response.status_code != 200:
        return render(request, 'auth/login.html', {
            'error': 'Failed to fetch user info from Google.',
            'form': LoginForm(),
        })

    user_info = userinfo_response.json()

    service = AuthService('google')
    result = service.authenticate(
        request,
        google_id=user_info['sub'],
        email=user_info['email'],
        name=user_info.get('name', ''),
        access_token=access_token,
        refresh_token=refresh_token,
    )

    if result.success:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'auth/login.html', {'error': result.error, 'form': LoginForm()})
