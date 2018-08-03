from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingFilterSortForm
# from django.shortcuts import render_to_response
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

class BookingEditTableView(TemplateView):
    
    def get_edit_table(request):
        template_name = 'edit_table.html'

        tmr = datetime.now() + timedelta(days=1)
        today = datetime.now()

        if request.method == "GET":
            form = BookingFilterSortForm(request.GET)
            date = request.GET.get("date")

            if date == None:
                date = ''

            if not date:
                bookings = Booking.objects.order_by('date', 'work_id')
            else:
                bookings = Booking.objects.filter(Q(date=date) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & Q(return_tr=''))).order_by('date', 'work_id')
        else:
            bookings = Booking.objects.order_by('date', 'work_id')

        return render(request, template_name, {'bookings': bookings, 'form': form, 'date': date, 'today': today, 'tmr': tmr})


    def save_edit_table(request):
        if request.method == 'POST':
            pk = dict(request.POST)['pk']
            time = dict(request.POST)['time']
            date = dict(request.POST)['date']
            pickup_tr = dict(request.POST)['pickup_tr']
            pickup_from = dict(request.POST)['pickup_from']
            forward_tr = dict(request.POST)['forward_tr']
            factory = dict(request.POST)['factory']
            backward_tr = dict(request.POST)['backward_tr']
            return_tr = dict(request.POST)['return_tr']
            return_to = dict(request.POST)['return_to']
            container_no = dict(request.POST)['container_no']
            seal_no = dict(request.POST)['seal_no']
            closing_date = dict(request.POST)['closing_date']
            closing_time = dict(request.POST)['closing_time']
            ref = dict(request.POST)['ref']
            remark = dict(request.POST)['remark']
            return_date = dict(request.POST)['return_date']

            for i in range(0,len(pk)):
                if not date[i]:
                    date[i] = None
                if not closing_date[i]:
                    closing_date[i] = None
                if not return_date[i]:
                    return_date[i] = None

                booking = Booking.objects.get(pk=pk[i])
                booking.time = time[i]
                booking.date = date[i]
                booking.pickup_tr = pickup_tr[i]
                booking.pickup_from = pickup_from[i]
                booking.factory = factory[i]
                booking.backward_tr = backward_tr[i]
                booking.return_tr = return_tr[i]
                booking.return_to = return_to[i]
                booking.container_no = container_no[i]
                booking.seal_no = seal_no[i]
                booking.closing_date = closing_date[i]
                booking.closing_time = closing_time[i]
                booking.ref = ref[i]
                booking.remark = remark[i]
                booking.return_date = return_date[i]
                booking.save()
            messages.success(request, "Saved Booking.")
            return redirect('booking-table')
        else:
            return redirect('booking-edit')
