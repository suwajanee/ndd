from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingAddForm
from django.shortcuts import render_to_response
from datetime import datetime
from django.db.models import Max
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

# class BookingAddView(CreateView):
#     model = Booking
#     fields = ('time', 'date', 'principal', 'shipper')
    # success_url = reverse_lazy('booking-add')


class BookingAddView(TemplateView):

    def add_booking(request):
        add_booking = BookingAddView()
        template_name = 'add_booking.html'
        context = {}
        context['form'] = BookingAddForm()
        context['principals'] = Principal.objects.all().order_by('name')
        if request.method == 'POST':
            context = add_booking.create_context(request.POST)
            
        return render(request, template_name, context)

    def create_context(self, req):
        context = {}
        # context['form'] = BookingAddForm()
        context['principals'] = Principal.objects.all().order_by('name')
        if 'principal' in req:
            # print(request.POST)
            context['principal'] = req.get('principal')
            if context['principal']:
                context['shippers'] = Shipper.objects.filter(principal=context['principal']).order_by('name')
            else:
                context['shippers'] = []

            req._mutable = True
            context['size'] = req.getlist('size')
            context['quantity'] = req.getlist('quantity')
            context['date'] = req.getlist('date')
            context['zip'] = zip(context['size'], context['quantity'], context['date'])

            req.update({'size':'', 'quantity':'', 'date':''})
            context['form'] = BookingAddForm(req)
        return context


    def save_booking(request):
        add_booking = BookingAddView()
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
                if address == 'other':
                    address_other = request.POST['address_other']

                container = zip(size, quantity, date)
                for s, q, d in container:
                    for i in range(int(q)):
                        
                        work_id, work_number = add_booking.run_work_id(d)

                        data = {
                            'principal': Principal.objects.get(pk=principal),
                            'shipper': Shipper.objects.get(pk=shipper),
                            'agent': agent,
                            'booking_no': booking_no,
                            'booking_color': booking_color,
                            'size': s,
                            'date': d,
                            'fw_fm': fw_fm,
                            'loading': loading,
                            'bw_to': bw_to,
                            'vessel': vessel,
                            'port': port,
                            'closing_date': closing_date,
                            'closing_time': closing_time,
                            'ref': ref,
                            'remark': remark,
                            'work_id': work_id,
                            'work_number': work_number,
                            'pickup_date': d,
                            'factory_date': d,
                            'return_date': d,
                            'address': address
                        }
                        if address == 'other':
                            data['address_other'] = address_other

                        booking = Booking(**data)
                        booking.save()

                messages.success(request, "Added Booking")
                return redirect('booking-table')
                # return render(request, 'table.html')
            messages.error(request, "Error")
        return redirect('booking-add')

                        
                
                

                


    def run_work_id(self, date):
        # print(date)
        work = Booking.objects.filter(date=date).aggregate(Max('work_number'))
        # print(work['work_number__max'])
        if work['work_number__max'] == None:
            work_number = 0
        else:
            work_number = work['work_number__max'] + 1
        work = str("{:03d}".format(work_number))
        # print(work)
        print('11111111111111111111111111')
        d = datetime.strptime(date, "%Y-%m-%d")
        work_id = d.strftime('%d')+d.strftime('%m')+d.strftime('%y')+work
        print(work_id)
        return work_id, work_number