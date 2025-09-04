from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

def send_appointment_notification(appointment):
    # Prepare messages
    subject = "Appointment Confirmation"
    
    email_message = f"""
Hi {appointment.name} 👋,

✅ Your appointment with Dr. {appointment.doctor_name} is confirmed!

🆔 Appointment ID: {appointment.id}
📅 Date: {appointment.appointment_date}
⏰ Time: {appointment.appointment_time}

📍 Location: Curovia Hospital, Kanyakumari

📝 Note: Please arrive 10 minutes early and bring your ID proof.

Thank you for trusting us! ❤️  
– Curovia Hospital Team
"""

    sms_message = (
        f"Hi {appointment.name}, your appointment with Dr. {appointment.doctor_name} "
        f"is confirmed on {appointment.appointment_date} at {appointment.appointment_time}. "
        f"ID: {appointment.id}. Please bring ID and arrive 10 mins early."
    )

    # --- Send Email ---
    try:
        send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [appointment.email])
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email sending failed:", e)

    # --- Send SMS using Twilio ---
    try:
        phone_number = str(appointment.phone_number)
        if not phone_number.startswith('+'):
            phone_number = '+91' + phone_number

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=sms_message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print("✅ SMS sent successfully:", sms.sid)
    except Exception as e:
        print("❌ SMS sending failed:", e)
