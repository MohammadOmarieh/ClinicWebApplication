from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView, )

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'nurses', NurseViewSet)
router.register(r'appointments', AppointmentViewSet)
# router.register(r'doctorappointments', DoctorAppointmentViewSet, basename='doctor-appointments')
urlpatterns = [
    # api urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls)),

    ##########################################################################
    # pages urls
    path('login', login, name='login'),
    path('api/user_register/', UserRegisterCreateAPIView.as_view(), name='apiregister'),
    path('api/doctor_register/', DoctorRegisterCreateAPIView.as_view(), name='userapiregister'),
    path('api/nurse_register/', NurseRegisterCreateAPIView.as_view(), name='nurseapiregister'),
    path('api/patient_register/', PatientRegisterCreateAPIView.as_view(), name='patientapiregister'),

    path('api/doctor_appointment/<int:doctor_id>/', DoctorAppointmentViewSet.as_view(), name='doctor_appointment'),
    path('api/patient_appointment/<int:patient_id>/', PatientAppointmentViewSet.as_view(), name='patient_appointment'),
    path('api/nurse_appointment/<int:nurse_id>/', NurseAppointmentViewSet.as_view(), name='nurse_appointment'),
    path('api/delete_appointment/<int:appointment_id>/', DeleteAppointment.as_view(), name='delete_appointment'),

    # path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('about', about, name='about'),
    path('services', services, name='services'),
    path('contactus', contactus, name='contactus'),
    path('add_appointment/(?P<user>.)/', add_appointment, name='add_appointment'),
    path('delete_appointment/(?P<user>.)/(?P<appointment_id>.)/', delete_appointment, name='delete_appointment'),
    path('dashboard/(?P<user>.)/', dashboard, name='dashboard'),
    # path('logout', logout, name='log  out'),
    path('', home, name='home'),
    path('email', send_email_view, name='email'),

]