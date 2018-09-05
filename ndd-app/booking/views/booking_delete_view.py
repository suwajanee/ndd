from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Booking


class BookingDeleteView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def delete_data_booking(request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.delete()

        if request.method == "GET":
            filter_by = request.GET.get("filter_by")
            date_filter = request.GET.get("date_filter")
            if not date_filter:
                return redirect(reverse('booking-table'))
            else:
                return redirect(reverse('booking-table') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)

    @login_required(login_url=reverse_lazy('login'))
    def delete_multiple_data_booking(request):
        
        if request.method == "POST":
            pk_list = request.POST.getlist('pk')
            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            for pk in pk_list:
                booking = Booking.objects.get(pk=pk)
                booking.delete()

            if not date_filter:
                return redirect(reverse('booking-table'))
            else:
                return redirect(reverse('booking-table') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)