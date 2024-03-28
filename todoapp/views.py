from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name = task)
        new_todo.save()
    todo_list = todo.objects.filter(user=request.user)
    context = {
        'todos': todo_list
    }
    return render(request, 'todoapp/homepage.html', context)
def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already Logged in.')
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        valid_username = User.objects.filter(username = username)
        if valid_username:
            messages.error(request, "User name already taken" )
            return redirect('register')

        if(password != confirm_password):
            messages.error(request, "The passwords donot match")
            return redirect('register')
        
        elif len(password) < 3:
            messages.error(request, 'The password must have three characters')
        else:
            new_user = User.objects.create_user(username=username , password=password ,email=email)
            new_user.save()
            messages.success(request, 'Account created successfully, Please login now')
            return redirect('login')
         

    return render(request, 'todoapp/register.html', {})
def edit_task(request, name):
    if request.method == "POST":
        task = request.POST.get('task')
        todo_instance = todo.objects.get(todo_name=name) 
        todo_instance.todo_name = task  
        todo_instance.save()  
        return redirect('home-page')

    return render(request, 'todoapp/edit.html')
def loginpage(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already Logged in.')
        return redirect('home-page')
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            messages.success(request, f" Welcome {username} ")
            return redirect('home-page')
        else:
            messages.error(request, 'Incorrect username or Password')
            return redirect('login')
    return render(request, 'todoapp/login.html', {})
@login_required
def delete_task(request , name):
    get_todo = todo.objects.get(user=request.user, todo_name = name)
    get_todo.delete()
    return redirect('home-page')
@login_required
def update_task(request,name):
    get_todo = todo.objects.get(user=request.user, todo_name = name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
def logout_user(request):
    logout(request)
    return redirect('login')
