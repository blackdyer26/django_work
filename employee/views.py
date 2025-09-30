from .forms import EmployeeForm, SignUpForm, SignInForm
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json

# API Configuration
# FIXED: Corrected the typo in the IP address from 1227.0.0.1 to 127.0.0.1
API_TOKEN_URL = "http://127.0.0.1:8001/api/token/"
API_REFRESH_URL = "http://127.0.0.1:8001/api/token/refresh/"
API_REGISTER_URL = "http://127.0.0.1:8001/api/register/"
API_BASE = "http://127.0.0.1:8001/api/employees/"

def signup_page(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the data payload to send to the API
            data = {
                "username": form.cleaned_data.get("username"),
                "email": form.cleaned_data.get("email"),
                "password": form.cleaned_data.get("password"),
                "confirm_password": form.cleaned_data.get("confirm_password"),
            }
            try:
                print(f"Attempting to register user: {data['username']}")  # Debug
                response = requests.post(API_REGISTER_URL, json=data, timeout=10)
                print(f"Registration response status: {response.status_code}")  # Debug
                print(f"Registration response content: {response.text}")  # Debug
                
                if response.status_code == 201:
                    messages.success(request, "Account created successfully! Please sign in.")
                    # In Django 5+, redirect can take the URL name directly
                    return redirect("employee:signin")
                else:
                    # Handle different error responses
                    if response.content:
                        try:
                            error_data = response.json()
                            if isinstance(error_data, dict):
                                # Handle field-specific errors
                                for field, errors in error_data.items():
                                    if isinstance(errors, list):
                                        for error in errors:
                                            messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
                                    else:
                                        messages.error(request, f"{field.title().replace('_', ' ')}: {errors}")
                            else:
                                messages.error(request, str(error_data))
                        except json.JSONDecodeError:
                            messages.error(request, f"Registration failed with status {response.status_code}. Please check server logs.")
                    else:
                        messages.error(request, "Registration failed. Please try again.")
            except requests.exceptions.ConnectionError as e:
                messages.error(request, f"Unable to connect to the API server. Please ensure the server is running on port 8001.")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
            # Display form validation errors from the Django form itself
            for field, errors in form.errors.items():
                for error in errors:
                    # Make the field name more readable
                    field_name = field.replace('_', ' ').title()
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def signin_page(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data.get("username"),
                "password": form.cleaned_data.get("password"),
            }
            try:
                print(f"Attempting to sign in user: {data['username']}")  # Debug
                headers = {"Content-Type": "application/json"}
                response = requests.post(API_TOKEN_URL, json=data, headers=headers, timeout=10)
                print(f"Sign in response status: {response.status_code}")  # Debug
                print(f"Sign in response content: {response.text}")  # Debug
                
                if response.status_code == 200:
                    tokens = response.json()
                    access_token = tokens.get("access")
                    refresh_token = tokens.get("refresh")
                    
                    if access_token:
                        messages.success(request, "Successfully signed in!")
                        # Assuming 'employee_list' is the name of your employee list page
                        res = redirect("employee:list") 
                        res.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
                        if refresh_token:
                            res.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
                        return res
                    else:
                        messages.error(request, "Invalid response from server.")
                elif response.status_code == 401:
                    messages.error(request, "Invalid username or password.")
                else:
                    # Handle other error responses
                    if response.content:
                        try:
                            error_data = response.json()
                            error_msg = error_data.get("detail", "Authentication failed.")
                            messages.error(request, error_msg)
                        except json.JSONDecodeError:
                             messages.error(request, f"Authentication failed with status {response.status_code}.")
                    else:
                        messages.error(request, "Authentication failed. Please try again.")
            except requests.exceptions.ConnectionError as e:
                messages.error(request, f"Unable to connect to the API server. Please ensure the server is running on port 8001.")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
    else:
        form = SignInForm()
    return render(request, "signin.html", {"form": form})

def signout_page(request):
    if request.method == "POST":
        res = redirect("employee:signin")
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        messages.success(request, "You have been signed out successfully.")
        return res
    return render(request, "signout.html")

def create(request):
    access_token = request.COOKIES.get("access_token")
    
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("employee:signin")
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            
            try:
                response = requests.post(API_BASE, json=data, headers=headers, timeout=10)
                if response.status_code == 201:
                    messages.success(request, "Employee created successfully.")
                    return redirect('employee:list')
                elif response.status_code == 401:
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("employee:signin")
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
                    # Generic error handling for other statuses
                    messages.error(request, f"Failed to create employee (Status: {response.status_code}).")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
    else:
        form = EmployeeForm()
    
    return render(request, 'create.html', {'form': form})

def list(request):
    access_token = request.COOKIES.get("access_token")
    
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("employee:signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    employees = []
    
    try:
        response = requests.get(API_BASE, headers=headers, timeout=10)
        if response.status_code == 200:
            employees = response.json()
        elif response.status_code == 401:
            messages.error(request, "Session expired. Please sign in again.")
            res = redirect("employee:signin")
            res.delete_cookie("access_token")
            res.delete_cookie("refresh_token")
            return res
        else:
            messages.error(request, f"Failed to fetch employees (Status: {response.status_code}).")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Could not connect to API server: {str(e)}")
    
    return render(request, 'list.html', {'employees': employees})

def update(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("employee:signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{pk}/"
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            headers["Content-Type"] = "application/json"
            
            try:
                response = requests.patch(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    messages.success(request, "Employee updated successfully.")
                    return redirect('employee:list')
                elif response.status_code == 401:
                    # Handle token expiration
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("employee:signin")
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
                    messages.error(request, f"Failed to update employee (Status: {response.status_code}).")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
            # If form is invalid, render the update page again with errors
            return render(request, 'update.html', {'form': form})
    else:
        # GET request: fetch existing data to populate the form
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                employee_data = response.json()
                form = EmployeeForm(initial=employee_data)
                return render(request, 'update.html', {'form': form})
            elif response.status_code == 401:
                messages.error(request, "Session expired. Please sign in again.")
                return redirect("employee:signin")
            else:
                messages.error(request, "Employee not found.")
                return redirect('employee:list')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
            return redirect('employee:list')

def delete(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("employee:signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{pk}/"
    
    if request.method == 'POST':
        try:
            response = requests.delete(url, headers=headers, timeout=10)
            if response.status_code == 204:
                messages.success(request, "Employee deleted successfully.")
            elif response.status_code == 401:
                messages.error(request, "Session expired. Please sign in again.")
                return redirect("employee:signin")
            else:
                messages.error(request, "Failed to delete employee.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
        return redirect('employee:list')
    else:
        # GET request, show confirmation page
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                employee = response.json()
                return render(request, 'delete.html', {'employee': employee})
            else:
                messages.error(request, "Employee not found.")
                return redirect('employee:list')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
            return redirect('employee:list')