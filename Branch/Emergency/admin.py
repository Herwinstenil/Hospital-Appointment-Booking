from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from .models import BackgroundImage, Appointment
from .utils import send_appointment_notification  

@admin.register(BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'doctor_name', 'appointment_date', 'appointment_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'doctor_name')
    search_fields = ('name', 'email', 'phone_number', 'doctor_name')

    def save_model(self, request, obj, form, change):
        if obj.is_confirmed and obj.appointment_date and obj.appointment_time:
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                send_appointment_notification(obj) 
        super().save_model(request, obj, form, change)
