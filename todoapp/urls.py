from django.urls import path
from .import views

urlpatterns = [
    path('',views.loginpage, name=''),
    path('home/',views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('delete-task/<str:name>/', views.delete_task, name='delete'),
    path('update-task/<str:name>/', views.update_task, name='update'),
    path('logout/', views.logout_user , name='logout-user'),
    path('edit/<str:name>/', views.edit_task, name="edit")
    
]