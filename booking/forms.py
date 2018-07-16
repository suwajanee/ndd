from django import forms
from datetime import datetime

class BookingFilterForm(forms.Form):
	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'onchange': 'this.form.submit();'
			}
		),
	)
	