from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingAddForm
from django.shortcuts import render_to_response
from datetime import datetime

# class BookingAddView(CreateView):
#     model = Booking
#     fields = ('time', 'date', 'principal', 'shipper')
    # success_url = reverse_lazy('booking-add')


class BookingAddView(TemplateView):

    def add_booking(request):
        template_name = 'add_booking.html'
        context = {}
        context['form'] = BookingAddForm()
        context['principals'] = Principal.objects.all().order_by('name')
        if 'principal' in request.POST:
            # print(request.POST)
            context['principal'] = request.POST.get('principal')
            if context['principal']:
                context['shippers'] = Shipper.objects.filter(principal=context['principal']).order_by('name')
            else:
                context['shippers'] = []

            request.POST._mutable = True
            context['size'] = request.POST.getlist('size')
            context['quantity'] = request.POST.getlist('quantity')
            context['date'] = request.POST.getlist('date')
            context['zip'] = zip(context['size'], context['quantity'], context['date'])

            request.POST.update({'size':'', 'quantity':'', 'date':''})
            context['form'] = BookingAddForm(request.POST)
        return render(request, template_name, context)


    def save_booking(request):
        if request.method == 'POST':
            form = BookingAddForm(request.POST)
            if form.is_valid():
                principal = request.POST['principal']
                shipper = request.POST['shipper']
                agent = request.POST['agent']
                booking_no = request.POST['booking_no']
                booking_color = request.POST['booking_color']
                size = request.POST.getlist('size')
                quantity = request.POST.getlist('quantity')
                date = request.POST.getlist('date')
                fw_fm = request.POST['fw_fm']
                loading = request.POST['loading']
                bw_to = request.POST['bw_to']
                vessel = request.POST['vessel']
                port = request.POST['port']
                closing_date = request.POST['closing_date']
                closing_time = request.POST['closing_time']
                ref = request.POST['ref']
                remark = request.POST['remark']
                address = request.POST['address']
                # address_other = request.POST['address_other']
                # print(datetime.strptime(date))

                for d in date :
                    
                    dd = datetime.strptime(d, "%Y-%m-%d")
                    print('11111111111111111111111111')
                    print(dd)

                data = {
                    principal: principal,

                }


        # p = Publisher(name='Apress', city='Berkeley')
        # p.save()