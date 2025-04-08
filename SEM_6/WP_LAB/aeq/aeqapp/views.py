from django.shortcuts import render
from .forms import BookingForm

# Create your views here.

def booking_view(request):
    message ='THIS ROOM IS BOOKED. PLEASE CHOOSE ANOTHER ROOM'
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():

            room = form.cleaned_data['room']
            if room.is_booked:
                message = 'THIS ROOM IS BOOKED. PLEASE CHOOSE ANOTHER ROOM'
                return render(request, 'status.html', {'message': message})
            room.is_booked = True
            room.save()
            message = 'Room booked successfully'
            return render(request,'status.html',{'message':message})
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})