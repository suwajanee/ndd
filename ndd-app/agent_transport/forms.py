from django import forms
# from customer.models import Principal, Shipper
from .models import AgentTransport


class AgentTransportAddForm(forms.Form):
	
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

	WORK_CHOICES = (
		('ep', 'Empty'),
		('fc', 'Full'),
	)
	work_type = forms.ChoiceField(
		choices=WORK_CHOICES,
		initial="empty",
		widget=forms.Select(
			attrs={
				'class': 'custom-select w-15',
			}
		),
		required=False
	)
	