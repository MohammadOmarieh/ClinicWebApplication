from django.contrib import admin
from .models import *


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'speciality', 'email', 'phone')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dob', 'address', 'phone', 'email')


class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'nurse', 'appoint_date', 'appoint_time', 'treatment')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Appointment, AppointmentAdmin)
