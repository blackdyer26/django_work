from django import forms

class UserRegisterForm(forms.Form):
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
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
        
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
