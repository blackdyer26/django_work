from django import forms

<<<<<<< HEAD
class UserRegisterForm(forms.Form):
=======
class SignUpForm(forms.Form):
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
    required=True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
<<<<<<< HEAD
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not confirm_password:
            raise forms.ValidationError("Please confirm your password.")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserLoginForm(forms.Form):
=======
)

def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    confirm_password = cleaned_data.get("confirm_password")

    if not confirm_password:
        raise forms.ValidationError("Please confirm your password.")
    if password != confirm_password:
        raise forms.ValidationError("Passwords do not match.")
    return cleaned_data


class SignInForm(forms.Form):
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
<<<<<<< HEAD
        
class EmployeeForm(forms.Form):
    employee_id = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    employee_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    employee_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    employee_contact = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
=======

class EmployeeForm(forms.Form):
    employee_id = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'})
    )
    employee_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Name'})
    )
    employee_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Employee Email'})
    )
    employee_contact = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'})
    )
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
