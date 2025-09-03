from django.shortcuts import render, redirect
from application.models import enquiry_table, enquiry_table_1
from datetime import datetime
from django.utils import timezone
from django.contrib import messages


def home(request):
    return render(request, 'index.html')


def starterpage(request):
    return render(request, 'starterpage.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        info = enquiry_table.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone="N/A",
            date=timezone.now(),
            time=timezone.now(),
            people=1
        )
        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')

    return render(request, 'contact.html')


def form(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            people = request.POST.get('people', 1)
            message = request.POST.get('message')
            subject = request.POST.get('subject', 'Table Booking')

            # Convert to timezone-aware datetime
            date_obj = timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
            time_obj = timezone.make_aware(datetime.strptime(time_str, "%H:%M"))

            enquiry_table_1.objects.create(
                name=name,
                email=email,
                phone=phone,
                date=date_obj,
                time=time_obj,
                people=int(people),
                message=message,
                subject=subject
            )

            messages.success(request, "Your table has been booked successfully!")
            return redirect('form')
        except Exception as err:
            messages.error(request, "Error submitting the form.")
            print("Form submission error:", err)

    return render(request, 'form.html')
