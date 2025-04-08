from django.shortcuts import render,redirect
from .models import Appointment,Doctor
from .forms import AppointmentForm, DoctorForm

# Create your views here.

def doctor_view(request):
    if request.method =='POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_view')
    else:
        form = DoctorForm()
    return render(request,'add_doctor.html',{'form':form})

def appointment_view(request):
    message ="BOOKED YOUR SLOT"
    if request.method =='POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data['patient_name']
            email = form.cleaned_data['email']
            doctor = form.cleaned_data['doctor']
            time_slot = form.cleaned_data['time_slot']
            if(Appointment.objects.filter(doctor = doctor,time_slot = time_slot).exists()):
                message = "SORRY THIS TIME SLOT HAS BEEN BOOKED"
            else:
                form.save()
                return  render(request,'status.html',{'form':form,'message':message})
    else:
        form = AppointmentForm()
    return render(request,'book_appointment.html',{'form':form,'message':message})