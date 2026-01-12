from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from datetime import timedelta
import os, json

from .models import enquiry_table, enquiry_table_1
from openai import OpenAI


# =========================
# 🌐 PUBLIC PAGES
# =========================

def home(request):
    return render(request, 'index.html')

def starterpage(request):
    return render(request, 'starterpage.html')

def contact(request):
    if request.method == 'POST':
        enquiry_table_1.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Enquiry submitted successfully")
        return redirect('contact')

    return render(request, 'contact.html')


# =========================
# 🍽️ TABLE BOOKING (USER)
# =========================

@login_required(login_url='login')
def form(request):
    if request.method == 'POST':
        enquiry_table.objects.create(
            name=request.user.username,
            email=request.user.email,
            phone=request.POST.get('phone'),
            subject="Table Booking",
            message=request.POST.get('message'),
            people=int(request.POST.get('people') or 1),
        )
        messages.success(request, "Table booked successfully")
        return redirect('user_dashboard')

    return render(request, 'form.html')


# =========================
# 🔐 AUTHENTICATION
# =========================

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )

        if request.POST.get("role") == "admin":
            user.is_staff = True
            user.save()

        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# 🔁 DASHBOARD REDIRECT
# =========================

@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')


# =========================
# 👤 USER DASHBOARD
# =========================

@login_required
def user_dashboard(request):
    bookings = enquiry_table.objects.filter(
        email=request.user.email
    ).order_by('-date')

    return render(request, 'user_dashboard.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        enquiry_table,
        id=booking_id,
        email=request.user.email
    )

    booking.status = 'cancelled'
    booking.save()

    messages.success(request, "Booking cancelled")
    return redirect('user_dashboard')


# =========================
# 🛠️ ADMIN DASHBOARD
# =========================

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')

    today_start = now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    context = {
        'bookings': enquiry_table.objects.all().order_by('-date'),
        'users': User.objects.filter(is_staff=False),
        'enquiries': enquiry_table_1.objects.all().order_by('-id')[:10],
        'total_bookings': enquiry_table.objects.count(),
        'today_bookings': enquiry_table.objects.filter(
            date__gte=today_start,
            date__lt=today_end
        ).count(),
        'cancelled_bookings': enquiry_table.objects.filter(status='cancelled').count(),
        'total_users': User.objects.filter(is_staff=False).count(),
    }

    return render(request, 'dashboard.html', context)


@login_required
def admin_add_booking(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        enquiry_table.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            people=request.POST.get('people'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Booking added")
        return redirect('admin_dashboard')

    return render(request, 'admin_add_booking.html')


@login_required
def admin_edit_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect('login')

    booking = get_object_or_404(enquiry_table, id=booking_id)

    if request.method == "POST":
        booking.people = request.POST.get('people')
        booking.message = request.POST.get('message')
        booking.status = request.POST.get('status')
        booking.save()

        messages.success(request, "Booking updated")
        return redirect('admin_dashboard')

    return render(request, 'admin_edit_booking.html', {'booking': booking})


@login_required
def admin_cancel_booking(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized")
        return redirect('login')

    booking = get_object_or_404(enquiry_table, id=booking_id)
    booking.status = 'cancelled'
    booking.save()

    messages.success(request, "Booking cancelled successfully")
    return redirect('admin_dashboard')


@login_required
@require_POST
def admin_delete_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect('login')

    enquiry_table.objects.filter(id=booking_id).delete()
    messages.success(request, "Booking deleted")
    return redirect('admin_dashboard')


# =========================
# 🤖 AI RECOMMENDATION
# =========================

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@login_required
def ai_recommend(request):
    recommendation = None
    error = None

    if request.method == "POST":
        try:
            prompt = f"""
Pure vegetarian Indian food recommendation.
Mood: {request.POST.get('mood')}
Spice: {request.POST.get('spice')}
Budget: {request.POST.get('budget')}

Return JSON only:
{{"starter":"","main":"","drink":"","reason":""}}
"""

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            recommendation = json.loads(res.choices[0].message.content)

        except Exception as e:
            error = str(e)

    return render(request, "ai_recommend.html", {
        "recommendation": recommendation,
        "error": error
    })
