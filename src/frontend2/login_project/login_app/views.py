# login_app/views.py
import os

from django.shortcuts import render, redirect
import requests
from datetime import datetime
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
            return redirect('success')
        else:
            # If not successful, show error message
            error = 'Login failed. Please try again.'

    return render(request, 'login.html', {'error': error})


import requests
from django.shortcuts import render
from datetime import datetime

def success(request):
    api_url = 'http://127.0.0.1:9091/get_students'
    response = requests.post(api_url)

    # Handle API response
    if response.status_code == 200:
        last_entries = {}

        for entry in response.json():
            student_name = entry["student_name"]
            timestamp_str = entry["timestamp"]
            image_base_64 = entry["image_base_64"]

            # Convert timestamp string to datetime object
            timestamp = datetime.strptime(timestamp_str.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")

            # Check if image_base_64 is not empty and update last_entries if newer timestamp found
            if image_base_64 and (student_name not in last_entries or timestamp > last_entries[student_name]["timestamp"]):
                last_entries[student_name] = {
                    "timestamp": timestamp,
                    "image_base_64": image_base_64,
                    "yawning": entry["yawning"],
                    "sleeping": entry["sleeping"],
                    "ago": int((datetime.now() - timestamp).total_seconds() // 60),
                }

        data = []
        for i in last_entries:
            cur = {
                "name": i,
                "timestamp": str(last_entries[i]["timestamp"]) + "(" + str(last_entries[i]["ago"]) + "minutes ago)",
                "image_base_64": last_entries[i]["image_base_64"],
                "yawning": last_entries[i]["yawning"],
                "sleeping": last_entries[i]["sleeping"],
            }
            data.append(cur)

        # Return the rendered template with the context
        return render(request, 'success.html', {'data': data})

    else:
        error = 'Login failed. Please try again.'
        # Debugging output (optional, for debugging purposes)
        print("Error: Login failed.")
        return render(request, 'success.html', {'error': error})
