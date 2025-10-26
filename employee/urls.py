from django.urls import path
from .views import signin_page, signout_page, signup_page ,create_employee, update_employee, employee_list, delete_employee

urlpatterns = [
    path('', signin_page, name="signin"),
    path('create/', create_employee, name="create"),
    path('list/', employee_list, name='list'),
    path('update/<int:pk>/', update_employee, name="update"),
    path('delete/<int:pk>/', delete_employee, name="delete"),
    path('signup/', signup_page, name='signup'),
    path('signin/', signin_page, name='signin'),
    path('signout/', signout_page, name='signout'),
]