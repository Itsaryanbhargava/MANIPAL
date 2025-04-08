
from django import forms
from .models import Room, Booking


class BookingForm(forms.ModelForm):

    room = forms.ModelChoiceField(
        queryset= Room.objects.all(),
        label = 'Select room',
        required=True
    )
    class Meta:
        model = Booking
        fields = ['name','email','room']
