from django.urls import path
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
]