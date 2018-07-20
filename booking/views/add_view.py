from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingAddForm
from django.shortcuts import render_to_response


# class BookingAddView(CreateView):
#     model = Booking
#     fields = ('time', 'date', 'principal', 'shipper')
    # success_url = reverse_lazy('booking-add')


class BookingAddView(TemplateView):

    def add_booking(request):
        template_name = 'add_booking.html'
        context = {}
        context['form'] = BookingAddForm()
        # form = BookingAddForm()
        context['principals'] = Principal.objects.all().order_by('name')
        if 'principal' in request.POST:
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
        # return render_to_response(template_name, {"form":form}, context)


