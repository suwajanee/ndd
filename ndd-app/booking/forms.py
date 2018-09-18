from django import forms
from datetime import datetime
from customer.models import Principal, Shipper
from .models import Booking


class BookingAddForm(forms.Form):

	time = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '10',
			}
		),
		required=False
	)

	agent = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '50',
			}
		),
		required=False
	)

	booking_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'autocomplete': 'off',
				'maxlength': '50',
			}
		),
		required=False
	)

	pickup_from = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '20',
			}
		),
		required=False
	)
	
	return_to = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '20',
			}
		),
		required=False
	)

	return_date = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'date',
				'class': 'form-control',
			}
		),
		required=False,
		disabled=True,
	)

	vessel = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '50',
			}
		),
		required=False
	)

	port = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '50',
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
				'class': 'form-control',
				'maxlength': '5',
			}
		),
		required=False
	)

	ref = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '150',
			}
		),
		required=False
	)

	remark = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '150',
			}
		),
		required=False
	)

	factory = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'maxlength': '20',
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
				'class': 'form-control',
			}
		),
		required=False
	)

	address_other = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'class': 'form-control',
			}
		),
		required=False
	)