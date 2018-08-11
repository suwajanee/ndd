from django import forms
from customer.models import Principal, Shipper
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