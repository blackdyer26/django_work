<<<<<<< HEAD
import requests , json
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmployeeForm, UserRegisterForm, UserLoginForm
from django.contrib import messages

API_BASE_URL = "http://127.0.0.1:8001/api/"

def signup_page(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            
            try:
                response = requests.post(API_BASE_URL + "register/", json=payload, timeout=10)
                
                if response.status_code == 201: 
                    messages.success(request, "Account created successfully! Please sign in.")
                    return redirect("signin")
                else:
                    try:
                        error_data = response.json()
                        if isinstance(error_data, dict):
                            for field, errors in error_data.items():
                                for error in errors:
                                    field_name = field.replace('_', ' ').title()
                                    messages.error(request, f"{field_name}: {error}")
                        else:
                            messages.error(request, str(error_data))
                    except json.JSONDecodeError:
                        messages.error(request, f"Registration failed due to a server error (Status: {response.status_code}).")

            except requests.exceptions.ConnectionError:
                messages.error(request, "Unable to connect to the API server. Please ensure the backend is running.")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = UserRegisterForm()
        
=======
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
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    return render(request, "signup.html", {"form": form})

def signin_page(request):
    if request.method == "POST":
<<<<<<< HEAD
        form = UserLoginForm(request.POST)
=======
        form = SignInForm(request.POST)
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
        if form.is_valid():
            data = {
                "username": form.cleaned_data.get("username"),
                "password": form.cleaned_data.get("password"),
            }
            try:
<<<<<<< HEAD
                print(f"Attempting to sign in user: {data['username']}") 
                headers = {"Content-Type": "application/json"}
                response = requests.post(API_BASE_URL + "token/", json=data, headers=headers, timeout=10)
                print(f"Sign in response status: {response.status_code}")  
                print(f"Sign in response content: {response.text}") 
=======
                print(f"Attempting to sign in user: {data['username']}")  # Debug
                headers = {"Content-Type": "application/json"}
                response = requests.post(API_TOKEN_URL, json=data, headers=headers, timeout=10)
                print(f"Sign in response status: {response.status_code}")  # Debug
                print(f"Sign in response content: {response.text}")  # Debug
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
                
                if response.status_code == 200:
                    tokens = response.json()
                    access_token = tokens.get("access")
                    refresh_token = tokens.get("refresh")
                    
                    if access_token:
<<<<<<< HEAD
                        messages.success(request, "Successfully signed out!")
                        res = redirect("list") 
=======
                        messages.success(request, "Successfully signed in!")
                        # Assuming 'employee_list' is the name of your employee list page
                        res = redirect("employee:list") 
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
                        res.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
                        if refresh_token:
                            res.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
                        return res
                    else:
                        messages.error(request, "Invalid response from server.")
                elif response.status_code == 401:
                    messages.error(request, "Invalid username or password.")
                else:
<<<<<<< HEAD
=======
                    # Handle other error responses
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
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
<<<<<<< HEAD
=======
            # Display form validation errors
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
    else:
<<<<<<< HEAD
        form = UserLoginForm()
=======
        form = SignInForm()
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    return render(request, "signin.html", {"form": form})

def signout_page(request):
    if request.method == "POST":
<<<<<<< HEAD
        res = redirect("signin")
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        return res
    return render(request, "signin.html")

def create_employee(request):
    access_token = request.COOKIES.get("access_token")
    refresh_token = request.COOKIES.get("refresh_token") # This is still unused

    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("signin")
=======
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
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
<<<<<<< HEAD
            headers = {"Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"}
            
            try:
                # Use base URL
                response = requests.post(API_BASE_URL + "employees/", json=data, headers=headers, timeout=10)
                if response.status_code == 201:
                    messages.success(request, "Employee created successfully.")
                    return redirect('list')
                elif response.status_code == 401:
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("signin")
=======
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            
            try:
                response = requests.post(API_BASE, json=data, headers=headers, timeout=10)
                if response.status_code == 201:
                    messages.success(request, "Employee created successfully.")
                    return redirect('employee:list')
                elif response.status_code == 401:
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("employee:signin")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
<<<<<<< HEAD
                    messages.error(request, f"Failed to create employee (Status: {response.status_code}).")
                    return render(request, 'create.html', {'form': form})
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
                return render(request, 'create.html', {'form': form})
=======
                    # Generic error handling for other statuses
                    messages.error(request, f"Failed to create employee (Status: {response.status_code}).")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
        else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
<<<<<<< HEAD
            return render(request, 'create.html', {'form': form})
=======
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    else:
        form = EmployeeForm()
    
    return render(request, 'create.html', {'form': form})

<<<<<<< HEAD
def employee_list(request):
=======
def list(request):
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    access_token = request.COOKIES.get("access_token")
    
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
<<<<<<< HEAD
        return redirect("signin")
=======
        return redirect("employee:signin")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    
    headers = {"Authorization": f"Bearer {access_token}"}
    employees = []
    
    try:
<<<<<<< HEAD
        # Use base URL
        response = requests.get(API_BASE_URL + "employees/", headers=headers, timeout=10)
=======
        response = requests.get(API_BASE, headers=headers, timeout=10)
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
        if response.status_code == 200:
            employees = response.json()
        elif response.status_code == 401:
            messages.error(request, "Session expired. Please sign in again.")
<<<<<<< HEAD
            res = redirect("signin")
=======
            res = redirect("employee:signin")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
            res.delete_cookie("access_token")
            res.delete_cookie("refresh_token")
            return res
        else:
            messages.error(request, f"Failed to fetch employees (Status: {response.status_code}).")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Could not connect to API server: {str(e)}")
    
    return render(request, 'list.html', {'employees': employees})

<<<<<<< HEAD
def update_employee(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    # Use base URL
    url = f"{API_BASE_URL}employees/{pk}/"
=======
def update(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("employee:signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{pk}/"
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            headers["Content-Type"] = "application/json"
            
            try:
                response = requests.patch(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    messages.success(request, "Employee updated successfully.")
<<<<<<< HEAD
                    return redirect('list')
                elif response.status_code == 401:
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("signin")
=======
                    return redirect('employee:list')
                elif response.status_code == 401:
                    # Handle token expiration
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("employee:signin")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
                    messages.error(request, f"Failed to update employee (Status: {response.status_code}).")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
<<<<<<< HEAD
            return render(request, 'update.html', {'form': form})

    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            employee_data = response.json()
            form = EmployeeForm(initial=employee_data)
            return render(request, 'update.html', {'form': form})
        elif response.status_code == 401:
            messages.error(request, "Session expired. Please sign in again.")
            return redirect("signin")
        else:
            messages.error(request, "Employee not found.")
            return redirect('list')
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Request failed: {str(e)}")
        return redirect('list')

def delete_employee(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    # Use base URL
    url = f"{API_BASE_URL}employees/{pk}/"
=======
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
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    
    if request.method == 'POST':
        try:
            response = requests.delete(url, headers=headers, timeout=10)
            if response.status_code == 204:
                messages.success(request, "Employee deleted successfully.")
            elif response.status_code == 401:
                messages.error(request, "Session expired. Please sign in again.")
<<<<<<< HEAD
                return redirect("signin")
=======
                return redirect("employee:signin")
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
            else:
                messages.error(request, "Failed to delete employee.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
<<<<<<< HEAD
        return redirect('list')
    else:
        # This GET block is still missing a 401 check
=======
        return redirect('employee:list')
    else:
        # GET request, show confirmation page
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                employee = response.json()
                return render(request, 'delete.html', {'employee': employee})
            else:
                messages.error(request, "Employee not found.")
<<<<<<< HEAD
                return redirect('list')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
            return redirect('list')
=======
                return redirect('employee:list')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
            return redirect('employee:list')
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
