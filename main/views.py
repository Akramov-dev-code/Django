from django.shortcuts import render, redirect,get_object_or_404
from main.models import Course,Students
from django.http import HttpRequest
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout # Buni tepaga qo'shing

def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('index')

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
    if not request.user.is_authenticated:
        return redirect('login')
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
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'main/product_detail.html', {'course': course})

def checkout(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == "POST":
        full_name = request.POST.get("full_name") # HTML dagi name="full_name" bo'lishi kerak
        phone = request.POST.get("phone")        # HTML dagi name="phone"
        telegram = request.POST.get("telegram")  # HTML dagi name="telegram"
        
        # 1. Talabani yaratish
        student = Students.objects.create(
            name=full_name,
            phone=phone,
            username=telegram
        )
        
        # 2. Talabani tanlangan kursga qo'shish (ManyToManyField)
        student.courses.add(course)
        
        # 3. Telegramga xabar yuborish (Sotib olingani haqida)
        msg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        text = (f"🔥 Yangi o'quvchi kursga yozildi!\n\n"
                f"📚 Kurs: {course.title}\n"
                f"👤 O'quvchi: {full_name}\n"
                f"📞 Tel: {phone}\n"
                f"✈️ Telegram: {telegram}")
        
        requests.get(msg_url, params={"chat_id": CHAT_ID, "text": text})
        
        messages.success(request, "Tabriklaymiz! Siz kursga muvaffaqiyatli yozildingiz.")
        return redirect('index')
        
    return render(request, 'main/checkout.html', {'course': course})
def about_developer(request):
    return render(request, "main/about.html")
from django.shortcuts import render, redirect, get_object_or_404
from .models import Students, Course

# Dashboard - barcha o'quvchilar ro'yxati
def dashboard(request):
    students = Students.objects.all().order_by('-created_at')
    return render(request, 'main/dashboard.html', {'students': students})

# O'quvchini o'chirish
def delete_student(request, pk):
    student = get_object_or_404(Students, pk=pk)
    student.delete()
    return redirect('dashboard')

# O'quvchini tahrirlash
def edit_student(request, pk):
    student = get_object_or_404(Students, pk=pk)
    courses = Course.objects.all()
    
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.phone = request.POST.get('phone')
        student.username = request.POST.get('telegram')
        # ManyToMany kurslarni yangilash
        selected_courses = request.POST.getlist('courses')
        student.courses.set(selected_courses)
        
        student.save()
        return redirect('dashboard')
        
    return render(request, 'main/edit_student.html', {
        'student': student,
        'courses': courses
    })
def add_student(request):
    courses = Course.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        telegram = request.POST.get('telegram')
        selected_courses = request.POST.getlist('courses')
        
        student = Students.objects.create(
            name=name,
            phone=phone,
            username=telegram
        )
        student.courses.set(selected_courses)
        return redirect('dashboard')
        
    return render(request, 'main/edit_student.html', {'courses': courses, 'add_mode': True})