import os

from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import viewsets
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.conf import settings
import jwt
from twilio.rest import Client
from django.conf import settings
import io
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def jwt_decoder(access_token):
    # Decoder

    secret_key = settings.SECRET_KEY
    algorithms = ['HS256']
    decoded = jwt.decode(access_token, secret_key, algorithms=algorithms)
    print('This is the decoder')
    print(decoded)
    print('This is the user id')
    print(decoded.get('user_id'))
    user_id = decoded.get('user_id')

    return user_id


def name_doctor(doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    return doctor.name


def is_doctor(user_id):
    try:
        doctor = Doctor.objects.get(user=user_id)
        print('This doctor from method')
        print(doctor.id)
        return doctor.id
    except:
        return None


def name_patient(patient_id):
    patient = Patient.objects.get(id=patient_id)
    return patient.name


def is_patient(user_id):
    try:
        patient = Patient.objects.get(user=user_id)
        print('This patient from method')
        print(patient.id)
        return patient.id
    except:
        return None


def name_nurse(nurse_id):
    nurse = Nurse.objects.get(id=nurse_id)
    return nurse.name


def is_nurse(user_id):
    try:
        nurse = Nurse.objects.get(user=user_id)
        print('This doctor from method')
        print(nurse.id)
        return nurse.id
    except:
        return None


# Create your views here.

def home(request):
    return render(request, 'home.html', {"user": None})


def about(request):
    return render(request, 'about.html', {'user': None})


def register(request):
    if request.method == 'POST':
        print(request.POST['role'])
        url = 'http://127.0.0.1:8000/api/user_register/'
        patient_urlRgister = 'http://127.0.0.1:8000/api/patient_register/'
        doctor_urlRgister = 'http://127.0.0.1:8000/api/doctor_register/'
        nurse_urlRgister = 'http://127.0.0.1:8000/api/nurse_register/'

        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=data)
        print("this is user id")
        user_id = response.json().get('id')
        print(user_id)

        if request.POST['role'] == 'doctor':
            print("doctor role entered")
            doctor_data = {
                'user': user_id,
                'name': fullname,
                'speciality': "null",
                'phone': phone,
                'email': email
            }
            response = requests.post(doctor_urlRgister, data=doctor_data)
        elif request.POST['role'] == 'doctor':
            nurse_data = {
                'user': user_id,
                'name': fullname,
                'phone': phone,

            }
            response = requests.post(nurse_urlRgister, data=nurse_data)
        else:
            patient_data = {
                'user': user_id,
                'name': fullname,
                'dob': dob,
                'phone': phone,
                'address': address,
                'email': email

            }
            response = requests.post(patient_urlRgister, data=patient_data)
        if response.status_code == 200:
            return render(request, 'login.html')
        else:
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')


def dashboard(request, user):
    print('in dashboard')
    # print(user)
    user_type = None

    user_id = jwt_decoder(user)
    doctor_id = None
    if is_patient(user_id) is not None:
        patient_id = is_patient(user_id)
        user_type = "p"
        # print("the patient name is")
        # print(name_patient(patient_id))
        # print("(dashboard) the user is patient")
        response = requests.get(f'http://127.0.0.1:8000/api/patient_appointment/{patient_id}/')
    elif is_doctor(user_id) is not None:
        doctor_id = is_doctor(user_id)
        user_type = 'd'
        # print("(dashboard) the user is doctor")
        response = requests.get(f'http://127.0.0.1:8000/api/doctor_appointment/{doctor_id}/')
    else:
        nurse_id = is_nurse(user_id)
        user_type = 'n'
        # print("(dashboard) the user is nurse")
        response = requests.get(f'http://127.0.0.1:8000/api/nurse_appointment/{nurse_id}/')

    # GET doctors, nurses, patients
    response_p = requests.get(f'http://127.0.0.1:8000/api/patients/')
    if response_p.status_code == 200:
        patients = response_p.json()
        # print(patients)
    else:
        patients = []
        # print('else else else ')

    response_d = requests.get(f'http://127.0.0.1:8000/api/doctors/')
    if response_d.status_code == 200:
        doctors = response_d.json()
        # print(doctors)
    else:
        doctors = []
        # print('else else else ')

    response_n = requests.get(f'http://127.0.0.1:8000/api/nurses/')
    if response_n.status_code == 200:
        nurses = response_n.json()
        # print(nurses)
    else:
        nurses = []
        # print('else else else ')

    print('fetching')
    # doctor_id = None
    doctorname = None
    if response.status_code == 200:
        appointments = response.json()
        # print(appointments)
        if len(appointments) != 0:
            doctor_id = appointments[0]['doctor']
            doctorname = name_doctor(doctor_id)
            # print('(first element)The doctor id is')
            # print(doctor_id)
            # appointments['doctor_name'] = name_doctor(appointments['doctor'])
            # appointments['doctor_patient'] = name_doctor(appointments['patient'])
            # appointments['doctor_nurse'] = name_doctor(appointments['nurse'])
            for item in appointments:
                item['doctor_name'] = name_doctor(item['doctor'])
                item['patient_name'] = name_patient(item['patient'])
                item['nurse_name'] = name_nurse(item['nurse'])
            # print("items done")
            # print(appointments)

        else:
            print("-----------------------------")
            print(doctor_id)
            if doctor_id is not None:
                doctorname = name_doctor(doctor_id)
            else:
                doctorname = ''
    else:
        appointments = []
        # print('else else else ')

    return render(request, 'dashboard.html',
                  {'user_type': user_type, 'appointments': appointments, 'nurses': nurses, 'user': user,
                   'doctors': doctors, 'patients': patients, 'doctor_id': doctor_id, 'doctorname': doctorname})


def add_appointment(request, user):
    if request.method == 'POST':
        url = 'http://127.0.0.1:8000/api/appointments/'
        patient = request.POST.get('patient')
        print(patient)
        doctor = request.POST.get('doctor')
        print(doctor)
        nurse = request.POST.get('nurse')
        print(nurse)
        date = request.POST.get('date')
        print(date)
        time = request.POST.get('time')
        print(time)
        treatment = request.POST.get('treatment')
        print(treatment)

        data = {
            'doctor': doctor,
            'patient': patient,
            'nurse': nurse,
            'appoint_date': date,
            'appoint_time': time,
            'treatment': treatment
        }

        response = requests.post(url, data=data)

        if response.status_code == 200 or response.status_code == 201:
            # email_subject = 'Test Email'
            # email_body = 'Hello, world!'
            # from_email = 'recruitsystem.webapp@gmail.com'
            # to_email = ['ahmadhss366@gmail.com', 'toemail@gmail.com']
            #
            # email = EmailMessage(email_subject, email_body, from_email, to_email)
            # email.send()

            # Send Email
            # send_email_view(request)

            # Send SMS message using twilio
            # account_sid = 'ACca7ab82a3f414daa104bd2ab1ad85c26'
            # auth_token = '7ade36cc65f9bfe4b855a52be78137c9'
            # client = Client(account_sid, auth_token)
            #
            # message = client.messages.create(
            #     from_='+12544142563',
            #     body='Hello Ahmad! your appointment email sent by email. PLEASE check your email!',
            #     to='+96176178123'
            # )
            #
            # print(message.sid)


            return redirect('dashboard', user=user)
        else:
            return render(request, 'signup.html')

    else:
        return render(request, 'login.html')


def services(request):
    return render(request, 'services.html', {"user": None})


def contactus(request):
    return render(request, 'contactus.html', {"user": None})


################################################


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = 'http://127.0.0.1:8000/api/token/'
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            # Get the access token
            access_token = response.json()['access']
            print('access token')
            print(access_token)

            user_id = jwt_decoder(access_token)
            print('user id is')
            print(user_id)

            return redirect('dashboard', user=access_token)

        else:
            error_message = response.content.decode('utf-8', )
            return JsonResponse({'error': error_message}, status=response.status_code)
    else:
        return render(request, 'login.html')


def delete_appointment(request, user, appointment_id):
    print("the app is is:-------------------------")
    print(appointment_id)
    url = f'http://127.0.0.1:8000/api/delete_appointment/{appointment_id}/'
    response = requests.delete(url)
    return redirect('dashboard', user=user)


# APIs
#######################################################################
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class DeleteAppointment(APIView):
    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)


# class DoctorAppointmentViewSet(APIView):
#     def get(self, request, doctor_id):
#         # Logic for handling GET request
#         appointments = Appointment.objects.filter(doctor=doctor_id)
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class PatientRegisterCreateAPIView(APIView):
#     def post(self, request):
#         serializer = PatientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class DoctorAppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#
#     def get_queryset(self):
#         doctor_id = self.kwargs['doctor_id']  # Assuming you are passing the doctor_id in the URL
#         queryset = Appointment.objects.filter(doctor_id=doctor_id)
#         return queryset


class UserRegisterCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorRegisterCreateAPIView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRegisterCreateAPIView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NurseRegisterCreateAPIView(APIView):
    def post(self, request):
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAppointmentViewSet(APIView):
    def get(self, request, doctor_id):
        # Logic for handling GET request
        appointments = Appointment.objects.filter(doctor=doctor_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientAppointmentViewSet(APIView):
    def get(self, request, patient_id):
        # Logic for handling GET request
        appointments = Appointment.objects.filter(patient=patient_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NurseAppointmentViewSet(APIView):
    def get(self, request, nurse_id):
        # Logic for handling GET request
        appointments = Appointment.objects.filter(nurse=nurse_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_email_view(request):
    # Render the HTML template to a string
    context = {
        'doctor_name': 'Dr. John Smith',
        'nurse_name': 'Nurse Jane Doe',
        'appointment_date': '2023-05-21',
        'appointment_time': '10:00 AM',
        'patient_name': 'John Doe',
        'patient_email': 'ahmadhss366@gmail.com',
        'clinic_name': 'ABC Medical Center',
        'clinic_address': '123 Main Street, City',
        'appointment_duration': '60 minutes',
        'appointment_type': 'Follow-up',
        'special_instructions': 'Please bring any recent test results.',
    }  # Add any necessary context variables
    html_content = render_to_string('email.html', context)

    # Generate PDF using xhtml2pdf
    pdf_content = generate_pdf(html_content)

    # Create the EmailMessage object
    subject = 'Hello from Clinic!'
    from_email = 'recruitsystem.webapp@gmail.com'
    print(context['patient_email'])
    to_email = [context['patient_email']]
    email = EmailMessage(subject, '', from_email, to_email)

    # Attach the PDF to the email
    email.attach('document.pdf', pdf_content, 'application/pdf')

    # Send the email
    email.send()

    return HttpResponse('Email sent successfully!')


def generate_pdf(html_content):
    result_pdf = io.BytesIO()

    # Generate PDF using xhtml2pdf
    pisa.CreatePDF(html_content, dest=result_pdf)

    return result_pdf.getvalue()


