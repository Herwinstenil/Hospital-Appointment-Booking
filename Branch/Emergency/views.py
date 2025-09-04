from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import BackgroundImage, Appointment
from .forms import AppointmentForm
from .utils import send_appointment_notification

def index(request):
    hospital_logo = BackgroundImage.objects.filter(name__iexact="Hospital Logo").first()
    booking_logo = BackgroundImage.objects.filter(name__iexact="Booking Logo").first()
    cardio_image = BackgroundImage.objects.filter(name__iexact="Cardio").first()
    neuro_image = BackgroundImage.objects.filter(name__iexact="Neuro").first()
    pedia_image = BackgroundImage.objects.filter(name__iexact="Pedia").first()
    doc_image = BackgroundImage.objects.filter(name__iexact="Doc").first()
    Newdoc_image = BackgroundImage.objects.filter(name__iexact="Newdoc").first()
    Nextdoc_image = BackgroundImage.objects.filter(name__iexact="Nextdoc").first()
    return render(request, "index.html", {'hospital_logo': hospital_logo, 'booking_logo': booking_logo, 'cardio_image': cardio_image, 'neuro_image': neuro_image, 'pedia_image': pedia_image, 'doc_image': doc_image, 'Newdoc_image': Newdoc_image, 'Nextdoc_image': Nextdoc_image })

def logout(request):
    auth_logout(request)
    return redirect('index')

def profile_success(request):
    return render(request, 'success.html')

def SigninPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request, 'signin.html', {'error': 'Passwords do not match.'})
        if not uname or not email or not pass1:
            return render(request, 'signin.html', {'error': 'All fields are required.'})

        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'signin.html', {'error': str(e)})

    return render(request, 'signin.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    return render(request, "login.html")

def user_profile(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment request submitted successfully.')
            return redirect('profile_success')
    else:
        form = AppointmentForm()
    return render(request, 'userprofile.html', {'form': form})

@staff_member_required
def confirm_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = "Confirmed"
        appointment.is_confirmed = True
        appointment.save()
        send_appointment_notification(appointment)
        messages.success(request, 'Appointment confirmed and message sent.')
        return redirect('/admin/')
    except Appointment.DoesNotExist:
        return HttpResponse("Appointment not found.", status=404)
