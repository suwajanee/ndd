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
				'value': 1,
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

	fw_fm = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-fw-fm',
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