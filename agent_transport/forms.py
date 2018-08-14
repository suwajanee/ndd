from django import forms
# from customer.models import Principal, Shipper
from .models import AgentTransport


class AgentTransportFilterSortForm(forms.Form):
	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'form-control',
				'onchange': 'this.form.submit();'
			}
		),
		required=False
	)


class AgentTransportAddForm(forms.Form):
	agent = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
			}
		),
		required=False
	)

	booking_no = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'autocomplete': 'off',
			}
		),
		required=False
	)

	booking_color = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'type': 'color',
				'class': 'form-control',
			}
		),
		required=False
	)

	pickup_from = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
			}
		),
		required=False
	)
	
	return_to = forms.CharField(
		widget=forms.TextInput(
			attrs={
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
				'class': 'form-control',
			}
		),
		required=False
	)

	WORK_CHOICES = (
		('empty', 'Empty'),
		('full', 'Full'),
	)
	work_type = forms.ChoiceField(
		choices=WORK_CHOICES,
		initial="empty",
		widget=forms.Select(
			attrs={
				'class': 'form-control',
			}
		),
		required=False
	)

	# ADDRESS_CHOICES = (
	# 	('shipper', 'Shipper'),
	# 	('other', 'Other'),
	# 	('none', 'None'),
	# )
	# address = forms.ChoiceField(
	# 	choices=ADDRESS_CHOICES,
	# 	initial="shipper",
	# 	widget=forms.RadioSelect(
	# 		attrs={
	# 			'class': 'form-control',
	# 		}
	# 	),
	# 	required=False
	# )

	# address_other = forms.CharField(
	# 	widget=forms.Textarea(
	# 		attrs={
	# 			'class': 'form-control',
	# 		}
	# 	),
	# 	required=False
	# )