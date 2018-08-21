# from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
# from django.utils import timezone
from ..models import Booking
# from customer.models import Principal, Shipper
# from ..forms import BookingFilterSortForm
# from django.shortcuts import render_to_response
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
# from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class BookingTimeTableView(TemplateView):
    
    @login_required(login_url=reverse_lazy('login'))
    def time_table(request):
        template_name = 'booking/booking_time_table.html'

        tmr = datetime.now() + timedelta(days=1)
        today = datetime.now()

        if request.method == "POST":
            
            pk_list = request.POST.getlist("check")
            date = request.POST['date']

            bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'work_id')

            request.session['pk_list'] = pk_list
            request.session['date'] = date

            return render(request, template_name, {'bookings': bookings, 'date':date, 'today': today, 'tmr': tmr})
        else:
            if request.session['pk_list']:
                pk_list = request.session['pk_list']
                date = request.session['date']
                bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'work_id')

                request.session['pk_list'] = pk_list
                request.session['date'] = date

                return render(request, template_name, {'bookings': bookings, 'date':date, 'today': today, 'tmr': tmr, 'nbar': 'booking-table'})
            else:
                date = request.GET.get("date")
                if not date:
                    return redirect('booking-table')
                else:
                    return redirect('booking-table' + '?date=' + date)



    @login_required(login_url=reverse_lazy('login'))
    def save_time_table(request):
        if request.method == 'POST':
            pk = request.POST.getlist('pk')
            pickup_in_time = request.POST.getlist('pickup_in_time')
            pickup_out_time = request.POST.getlist('pickup_out_time')
            factory_in_time = request.POST.getlist('factory_in_time')
            factory_load_start_time = request.POST.getlist('factory_load_start_time')
            factory_load_finish_time = request.POST.getlist('factory_load_finish_time')
            factory_out_finish = request.POST.getlist('factory_out_finish')
            return_in_time = request.POST.getlist('return_in_time')
            return_out_time = request.POST.getlist('return_out_time')

            # pk = request.POST['pk']
            # pickup_in_time = request.POST['pickup_in_time']
            # pickup_out_time = request.POST['pickup_out_time']
            # factory_in_time = request.POST['factory_in_time']
            # factory_load_start_time = request.POST['factory_load_start_time']
            # factory_load_finish_time = request.POST['factory_load_finish_time']
            # factory_out_finish = request.POST['factory_out_finish']
            # return_in_time = request.POST['return_in_time']
            # return_out_time = request.POST['return_out_time']
            
            date_filter = request.POST['date_filter']


            for i in range(0,len(pk)):
                booking = Booking.objects.get(pk=pk[i])
                booking.pickup_in_time = pickup_in_time[i]
                booking.pickup_out_time = pickup_out_time[i]
                booking.factory_in_time = factory_in_time[i]
                booking.factory_load_start_time = factory_load_start_time[i]
                booking.factory_load_finish_time = factory_load_finish_time[i]
                booking.factory_out_finish = factory_out_finish[i]
                booking.return_in_time = return_in_time[i]
                booking.return_out_time = return_out_time[i]
                
                booking.save()

            messages.success(request, "Saving Booking.")
            return redirect(reverse('booking-time'))
        else:
            return redirect('booking-table')