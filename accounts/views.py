from django.shortcuts import render


def login_view(request):
    return render(request, "accounts/login.html")

# Logout view
def logout_view(request):
    pass

# register page
def register(request):    
    return render(request, "accounts/register.html")

# Profile page
def profile(request, username):
    pass
