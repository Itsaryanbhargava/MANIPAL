from django import forms 
from .models import Doctor, Appointment

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization']

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select a doctor")

    class Meta:
        model =Appointment
        fields = ['patient_name', 'email', 'doctor', 'time_slot']