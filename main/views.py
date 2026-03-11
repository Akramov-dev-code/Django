from django.shortcuts import render, redirect
from main.models import Course
from django.http import HttpRequest
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages


TOKEN = "8553368129:AAEBEtfmX-MCwYwngB-v6I3rpqAfq7Kv5UM"
CHAT_ID = "-1003813831969"


def register_view(request: HttpRequest):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bunday username mavjud")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bunday email mavjud")
            return redirect("register")

        if password1 != password2:
            messages.warning(request, "Parollar mos emas!")
            return redirect("register")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Muvaffaqqiyatli ro'yxatdan o'tdingiz!")
        return redirect("login")




    return render(request, "main/register.html")



def login_view(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Login yoki parol xato!")
            return redirect("login")
        
        login(request, user)
        return redirect("index")


    return render(request, "main/login.html")



def index_view(request: HttpRequest):
    if request.method == "POST":
        course_name = request.POST.get("course_name", "Unknown")
        course_price = request.POST.get("course_price", 0)
        discount_type = request.POST.get("discount_type", "flex")
        discount = request.POST.get("discount", 0)
        course = Course.objects.create(
            title=course_name,
            price=course_price,
            discount_type=discount_type,
            discount=discount
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        text = f"Yangi kurs yaratildi sayt orqali\nKurs nomi: {course_name}\nKurs narxi: {course_price}"

        requests.get(url=url, params={
            "chat_id": CHAT_ID,
            "text": text
        })

        return redirect("index")
    

    courses = Course.objects.all()

    search = request.GET.get("search", None)

    price_from = request.GET.get("price_from", None)
    price_to = request.GET.get("price_to", None)
    if price_from or price_to:
        courses = Course.objects.filter(price__gte=price_from, price__lte=price_to)
    if search:
        courses = Course.objects.filter(title__icontains=search)

    context = {
        "courses": courses,
        "search": search if search else ""
    }
    return render(request, "main/index.html", context)


def course_detail(request, pk):
    try:
        course = Course.objects.get(id=pk)
    except Exception as err:
        course = None
    context = {
        "course": course
    }
    return render(request, "main/course_detail.html", context)


def about_developer(request):
    return render(request, "main/about.html")