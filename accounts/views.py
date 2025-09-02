from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            # ✅ Check if user exists before authentication
            if not User.objects.filter(username=username).exists():
                messages.error(request, "User does not exist. Please register first.")
                return redirect("register")  # ✅ send to register page

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "accounts/loggedin.html", {"user": user})  # logged-in page
            else:
                return render(request, "accounts/login.html", {"error": "Invalid password"})
        else:
            return render(request, "accounts/login.html", {"error": "Please fill all fields"})
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    return render(request, "accounts/register.html")


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        return render(request, "accounts/profile.html", {"profile_user": user})
    except User.DoesNotExist:
        messages.error(request, "User not found. Please register.")
        return redirect("register")
