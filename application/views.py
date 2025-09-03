from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import enquiry_table, enquiry_table_1  
from django.utils.timezone import now

from .models import enquiry_table, SafeName

from django.core.paginator import Paginator
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'index.html')


def starterpage(request):
    return render(request, 'starterpage.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        
        enquiry_table_1.objects.create(
                name=name, email=email, phone=phone, subject=subject, message=message
        )
        messages.success(request, "Your enquiry was submitted successfully!")
        # except Exception as exc:
        #     messages.error(request, "Failed to submit enquiry: %s" % exc)
        return redirect('contact')
    return render(request, 'contact.html')




def form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        people = request.POST.get('people') or request.POST.get('person') or request.POST.get('guests') or 0
        
        enquiry_table.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message, people=int(people) if str(people).isdigit() else 0
        )
        messages.success(request, "Your table booking was successful!")
        return redirect('form')
    return render(request, 'form.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful. Welcome!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Logged out.')
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    # Count total reservations (enquiry_table)
    total_reservations = enquiry_table.objects.count()

    # Count total contacts (enquiry_table_1)
    total_contacts = enquiry_table_1.objects.count()

    # Count today's visitors (based on date in enquiry_table)
    todays_visitors = enquiry_table.objects.filter(date__date=now().date()).count()

    context = {
        'total_reservations': total_reservations,
        'total_contacts': total_contacts,
        'todays_visitors': todays_visitors,
        'recent_bookings': enquiry_table.objects.order_by('-date')[:5],  # latest 5
    }
    return render(request, 'dashboard.html', context)
@login_required(login_url='login')
def submissions(request):
    # Only allow staff (admin)
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to view submissions.")
        return redirect('dashboard')
    # Fetch bookings and enquiries with simple pagination
    bookings_qs = enquiry_table.objects.order_by('-date')
    contacts_qs = enquiry_table_1.objects.order_by('-date')
    bookings_page = request.GET.get('bpage', 1)
    contacts_page = request.GET.get('cpage', 1)
    bookings = Paginator(bookings_qs, 10).get_page(bookings_page)
    contacts = Paginator(contacts_qs, 10).get_page(contacts_page)
    return render(request, 'submissions.html', {'bookings': bookings, 'contacts': contacts})
