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
        
    return render(request, "signup.html", {"form": form})

def signin_page(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data.get("username"),
                "password": form.cleaned_data.get("password"),
            }
            try:
                print(f"Attempting to sign in user: {data['username']}") 
                headers = {"Content-Type": "application/json"}
                response = requests.post(API_BASE_URL + "token/", json=data, headers=headers, timeout=10)
                print(f"Sign in response status: {response.status_code}")  
                print(f"Sign in response content: {response.text}") 
                
                if response.status_code == 200:
                    tokens = response.json()
                    access_token = tokens.get("access")
                    refresh_token = tokens.get("refresh")
                    
                    if access_token:
                        messages.success(request, "Successfully signed out!")
                        res = redirect("list") 
                        res.set_cookie("access_token", access_token, httponly=True, samesite="Strict")
                        if refresh_token:
                            res.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
                        return res
                    else:
                        messages.error(request, "Invalid response from server.")
                elif response.status_code == 401:
                    messages.error(request, "Invalid username or password.")
                else:
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
    else:
        form = UserLoginForm()
    return render(request, "signin.html", {"form": form})

def signout_page(request):
    if request.method == "POST":
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
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
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
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
                    messages.error(request, f"Failed to create employee (Status: {response.status_code}).")
                    return render(request, 'create.html', {'form': form})
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
                return render(request, 'create.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{field.title().replace('_', ' ')}: {error}")
            return render(request, 'create.html', {'form': form})
    else:
        form = EmployeeForm()
    
    return render(request, 'create.html', {'form': form})

def employee_list(request):
    access_token = request.COOKIES.get("access_token")
    
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    employees = []
    
    try:
        # Use base URL
        response = requests.get(API_BASE_URL + "employees/", headers=headers, timeout=10)
        if response.status_code == 200:
            employees = response.json()
        elif response.status_code == 401:
            messages.error(request, "Session expired. Please sign in again.")
            res = redirect("signin")
            res.delete_cookie("access_token")
            res.delete_cookie("refresh_token")
            return res
        else:
            messages.error(request, f"Failed to fetch employees (Status: {response.status_code}).")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Could not connect to API server: {str(e)}")
    
    return render(request, 'list.html', {'employees': employees})

def update_employee(request, pk):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        messages.warning(request, "Please sign in to access this page.")
        return redirect("signin")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    # Use base URL
    url = f"{API_BASE_URL}employees/{pk}/"
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            headers["Content-Type"] = "application/json"
            
            try:
                response = requests.patch(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    messages.success(request, "Employee updated successfully.")
                    return redirect('list')
                elif response.status_code == 401:
                    messages.error(request, "Session expired. Please sign in again.")
                    res = redirect("signin")
                    res.delete_cookie("access_token")
                    res.delete_cookie("refresh_token")
                    return res
                else:
                    messages.error(request, f"Failed to update employee (Status: {response.status_code}).")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {str(e)}")
        else:
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
    
    if request.method == 'POST':
        try:
            response = requests.delete(url, headers=headers, timeout=10)
            if response.status_code == 204:
                messages.success(request, "Employee deleted successfully.")
            elif response.status_code == 401:
                messages.error(request, "Session expired. Please sign in again.")
                return redirect("signin")
            else:
                messages.error(request, "Failed to delete employee.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
        return redirect('list')
    else:
        # This GET block is still missing a 401 check
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                employee = response.json()
                return render(request, 'delete.html', {'employee': employee})
            else:
                messages.error(request, "Employee not found.")
                return redirect('list')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
            return redirect('list')
# Commit on 2025-10-20 14:10:00: authentication for frontend

# Commit on 2025-10-30 19:00:00: Fixed layout issues and optimized API calls
