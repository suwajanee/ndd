from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingFilterSortForm
# from django.shortcuts import render_to_response
from datetime import datetime, timedelta, date
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class BookingTableView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def get_table(request):
        template_name = 'booking/booking_table.html'

        tmr = datetime.now() + timedelta(days=1)
        today = datetime.now()

        if request.method == "GET":
            form = BookingFilterSortForm(request.GET)
            date = request.GET.get("date")

            if date == None:
                date = ''

            if not date:
                bookings = Booking.objects.filter(Q(date__month=today.month) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
            else:
                bookings = Booking.objects.filter(Q(date=date) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & (Q(return_tr='') & ~Q(cancel='1')))).order_by('date', 'work_id')
        else:
            bookings = Booking.objects.filter(date__month=today.month | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')

        return render(request, template_name, {'bookings': bookings, 'form': form, 'date': date, 'today': today, 'tmr': tmr, 'nbar': 'booking-table'})

    @login_required(login_url=reverse_lazy('login'))
    def delete_data(request, pk):
        delete_booking = BookingTableView()
        booking = Booking.objects.get(pk=pk)
        booking.delete()

        if request.method == "GET":
            date = request.GET.get("date")
            if not date:
                return redirect(reverse('booking-table'))
            else:
                return redirect(reverse('booking-table') + '?date=' + date)
    
    # def work_id_after_delete(self, booking):
    #     date = booking.date
    #     re_work_id = Booking.objects.filter(date=date, work_number__gt=booking.work_number)
    #     if re_work_id:
    #         for work in re_work_id:               
    #             new_work_number = work.work_number - 1
    #             work_str = str("{:03d}".format(new_work_number))
    #             work_id = date.strftime('%d')+date.strftime('%m')+date.strftime('%y')+work_str

    #             booking = Booking.objects.get(pk=work.pk)
    #             booking.work_id = work_id
    #             booking.work_number = new_work_number
    #             booking.save()
    #     return None
    @login_required(login_url=reverse_lazy('login'))
    def update_data(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            vessel = request.POST['vessel']
            port = request.POST['port']
            
            address = request.POST['address'+pk]
            if address == 'other':
                address_other = request.POST['address_other']

            cancel = request.POST['cancel']

            date_filter = request.POST['date_filter']

            booking = Booking.objects.get(pk=pk)
            booking.vessel = vessel
            booking.port = port
            booking.address = address
            if address == 'other':
                booking.address_other = address_other
            booking.cancel = cancel
            booking.save()

            messages.success(request, "Updated Booking.")
            return redirect(reverse('booking-table') + '?date=' + date_filter)
        else:
            return redirect('booking-table')
