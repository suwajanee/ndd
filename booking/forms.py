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
				'class': 'add-edit-form add-time form-control',
			}
		),
		required=False
	)

	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'add-edit-form add-date form-control',
				'placeholder': 'DATE',
			}
		)
	)

	agent = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-agent form-control',
			}
		),
		required=False
	)
	
	size = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-size form-control',
				'placeholder': 'SIZE',
			}
		),
	)

	quantity = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'number',
				'min': 1,
				'placeholder': 'QUANTITY',
				'class': 'add-edit-form add-quantity form-control',
			}
		)
	)

	booking_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-booking-no form-control',
				'autocomplete': 'off',
			}
		),
		required=False
	)

	booking_color = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'color',
				'class': 'add-edit-form add-booking-color form-control',
			}
		),
		required=False
	)

	fw_fm = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-fw-fm form-control',
			}
		),
		required=False
	)
	
	bw_to = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-bw-to form-control',
			}
		),
		required=False
	)

	vessel = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-vessel form-control',
			}
		),
		required=False
	)

	port = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-port form-control',
			}
		),
		required=False
	)

	closing_date = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'date',
				'class': 'form-control',
			}
		),
		required=False
	)

	closing_time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'time',
				'class': 'form-control',
			}
		),
		required=False
	)

	ref = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
			}
		),
		required=False
	)

	remark = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-remark form-control',
			}
		),
		required=False
	)

	loading = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'add-edit-form add-loading form-control',
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
				'class': 'add-address form-control',
			}
		),
		required=False
	)

	address_other = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'class': 'add-edit-form add-address-other form-control',
			}
		),
		required=False
	)