from django import forms
from datetime import datetime
from customer.models import Principal, Shipper
from .models import Booking


class BookingFilterForm(forms.Form):
	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'onchange': 'this.form.submit();'
			}
		),
	)

class BookingAddForm(forms.Form):

	time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-time',
			}
		),
		required=False
	)

	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'add-edit-form add-date',
			}
		)
	)

	agent = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-agent',
			}
		),
		required=False
	)
	
	size = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-size',
			}
		),
		required=False
	)

	quantity = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'number',
				'min': 1,
				'class': 'add-edit-form add-quantity',
			}
		)
	)

	booking_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-booking-no',
			}
		),
		required=False
	)

	booking_color = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'color',
				'class': 'add-edit-form add-booking-color',
			}
		),
		required=False
	)

	fw_tr = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-fw-tr',
			}
		),
		required=False
	)

	fw_fm = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-fw-fm',
			}
		),
		required=False
	)

	container_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-container-no',
			}
		),
		required=False
	)

	seal_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-seal-no',
			}
		),
		required=False
	)

	bw_tr = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-bw-tr',
			}
		),
		required=False
	)
	
	bw_to = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-bw-to',
			}
		),
		required=False
	)

	vessel = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-vessel',
			}
		),
		required=False
	)

	port = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-port',
			}
		),
		required=False
	)

	closing_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-closing-time',
			}
		),
		required=False
	)

	remark = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-remark',
			}
		),
		required=False
	)

	loading = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-loading',
			}
		),
		required=False
	)

	work_id = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-work-id',
			}
		),
		required=False
	)

	pickup_date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'add-edit-form add-pickup-date',
			}
		),
		required=False
	)

	factory_date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'add-edit-form add-factory-date',
			}
		),
		required=False
	)

	return_date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'add-edit-form add-return-date',
			}
		),
		required=False
	)

	pickup_in_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-pickup-in-time',
			}
		),
		required=False
	)
	
	pickup_out_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-pickup-out-time',
			}
		),
		required=False
	)
	
	factory_in_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-factory-in-time',
			}
		),
		required=False
	)
	
	factory_load_start_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-factory-load-start-time',
			}
		),
		required=False
	)

	factory_load_finish_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-factory-load-finish-time',
			}
		),
		required=False
	)

	factory_out_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-factory-out-time',
			}
		),
		required=False
	)

	return_in_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-return-in-time',
			}
		),
		required=False
	)
	
	return_out_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-return-out-time',
			}
		),
		required=False
	)

	ADDRESS_CHOICES = (
		('shipper', 'Shipper'),
		('other', 'Other'),
		('none', 'None'),
	)
	address = forms.ChoiceField(
		choices=ADDRESS_CHOICES,
		initial="shipper",
		widget=forms.RadioSelect(
			attrs={
				'class': 'add-address',
			}
		),
		required=False
	)

	address_other = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'class': 'add-edit-form add-address-other',
			}
		),
		required=False
	)