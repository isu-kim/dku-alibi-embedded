# login_app/views.py
import os

from django.shortcuts import render, redirect
import requests
from .models import users

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, '../templates'),
)


def login(request):
    error = None
    if request.method == 'POST':
        # Assuming the API endpoint for authentication
        api_url = 'http://127.0.0.1:9091/login'

        # Extract username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Make a POST request to the external API server
        response = requests.post(api_url, json={'username': username, 'password': password})

        # Handle API response
        if response.status_code == 200:
            # If successful, redirect to success page
            return redirect('success', username=username)
        else:
            # If not successful, show error message
            error = 'Login failed. Please try again.'

    return render(request, 'login.html', {'error': error})


def success(request, username):
    return render(request, 'success.html', {'username': username})
