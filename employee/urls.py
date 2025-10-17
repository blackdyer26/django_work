from django.urls import path
<<<<<<< HEAD
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
=======
from .views import (
    create,
    list,
    update,
    delete,
    signin_page,
    signup_page,
    signout_page,
)
from . import views

app_name = 'employee'

urlpatterns = [
    # Authentication URLs
    path('', views.signin_page, name='signin'),
    path('signin/', signin_page, name='signin'),
    path('signup/', signup_page, name='signup'),
    path('signout/', signout_page, name='signout'),
    
    # Employee management URLs - API endpoints
    path('api/employees/', list, name='list'),
    path('api/employees/create/', create, name='create'),
    path('api/employees/<int:pk>/update/', update, name='update'),
    path('api/employees/<int:pk>/delete/', delete, name='delete'),
>>>>>>> 81c30c68e201b27ff25fd8df7db601abd3a4824a
]