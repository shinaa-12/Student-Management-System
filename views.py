from django.shortcuts import render,redirect
from .models import Student
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    
    return render(request,'app1/home.html')


def insert_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if first_name and last_name and email and phone:
            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            messages.success(request," inserted successfully")
        else:
            messages.error(request, "All fields are required!")
    return render(request, 'app1/insert.html')


@login_required(login_url='login')
def display_view(request):
    data = Student.objects.all() 
    context = {'data': data}
    return render(request, 'app1/display.html', context)


@login_required(login_url='login')
def edit_view(request, s_id):
    obj = Student.objects.get(s_id=s_id)
    if request.method =='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email =request.POST.get('email')
        phone=int(request.POST.get('phone'))
        
        obj.first_name=first_name
        obj.last_name=last_name
        obj.email=email
        obj.phone=phone
        
        obj.save()
        context = {"msg":'student updated successfully.!'}
        return redirect('/display-student/')
    
    
    context = {'student':obj}
    return render(request, 'app1/edit.html', context)


@login_required(login_url='login')
def delete_view(request,s_id):
    obj = Student.objects.get(s_id=s_id)
    
    if request.method == 'POST':
        obj.delete()
        return redirect('/display-student/')
    
    
    context={'student':obj}
    return render(request,'app1/delete.html',context)




def login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("home")  
        else:
            context["login_error"] = "Invalid Username or Password"

    return render(request, "app1/login.html", context)


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            return render(request, "app1/register.html", {
                "error": "All fields are required"
            })

        if password != confirm_password:
            return render(request, "app1/register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "app1/register.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "app1/register.html", {
                "error": "Email already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        return render(request, "app1/register.html", {
            "success": "Registration successful! You can now login."
        })

    return render(request, "app1/register.html")


def logout_view(request):
    logout(request)
    return redirect('login')
    


