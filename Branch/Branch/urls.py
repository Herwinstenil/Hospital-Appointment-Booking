from django.contrib import admin
from django.urls import path
from Emergency import views
from django.conf.urls.static import static
from django.conf import settings
from Emergency.views import logout, confirm_appointment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  
    path('signin', views.SigninPage, name="signin"),
    path('login/', views.login_view, name="login"),
    path('logout/', logout, name="logout"),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('profile_success/', views.profile_success, name='profile_success'),
    path('confirm-appointment/<int:appointment_id>/', confirm_appointment, name='confirm_appointment'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
