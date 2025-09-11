from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Address
from products.models import Category
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from orders.models import Order
from django.contrib import messages
from .models import EmailOTP
import random


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to homepage or dashboard
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, password=password,email=email)
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    return render(request, "accounts/register.html")


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        categories = Category.objects.all()
        return render(request, "accounts/profile.html", {"profile_user": user,"categories": categories})
    except User.DoesNotExist:
        messages.error(request, "User not found. Please register.")
        return redirect("register")
    

def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "send_otp.html", {"error": "Email not registered"})

        otp = str(random.randint(100000, 999999))  # 6 digit OTP
        EmailOTP.objects.update_or_create(user=user, defaults={"otp": otp})

        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}. It will expire in 5 minutes.",
            "yourgmail@gmail.com",
            [email],
        )

        request.session["otp_user_id"] = user.id
        messages.success(request, "OTP sent successfully! Please check your email.")
        return redirect("verify_otp")

    return render(request, "accounts/otp.html")

def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        user_id = request.session.get("otp_user_id")

        if not user_id:
            return redirect("send_otp")

        user = User.objects.get(id=user_id)
        otp_record = EmailOTP.objects.filter(user=user).first()

        if otp_record and otp_record.otp == otp_entered:
            # OTP correct
            login(request, user)
            return redirect('home')
        else:
            return render(request, "accounts/verifyotp.html", {"error": "Invalid or expired OTP"})

    return render(request, "accounts/verifyotp.html")



@login_required
def profile_page(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(user=request.user).order_by('-placed_at')  # Fetch user orders
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        # Update user's name if "name" is submitted (optional: split into first/last)
        name = request.POST.get("name", "").strip()
        if name:
            if ' ' in name:
                request.user.first_name, request.user.last_name = name.split(' ', 1)
            else:
                request.user.first_name = name
                request.user.last_name = ""
        request.user.email = request.POST.get("email", request.user.email)
        request.user.save()
        profile.phone_number = request.POST.get("phone_number", profile.phone_number)
        # Checkbox: checked if present, False if not
        profile.promotions = 'promotions' in request.POST
        profile.save()
        return redirect("profile_page")
    return render(request, "accounts/profile.html", { "profile": profile, "categories": categories,"orders": orders,})


