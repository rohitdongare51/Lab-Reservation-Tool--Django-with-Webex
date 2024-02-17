from django import forms
from .models import Testbed


# class MyPostTestbed(forms.ModelForm):
	
# 	# template_name = 'testbeds/testbed_form.html/' 
# 	class Meta:
# 		model = Testbed
# 		fields = ['device','location', 'telnet', 'ssh']

# 		OPTIONS = [
# 		('sjc15', 'sjc15'),
# 		('sjc16', 'sjc16'),
# 		('ful', 'ful'),
# 		]
# 		selected_option = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))


class MyPostTestbed(forms.Form):
	
	class Meta:
		model = Testbed
		fields = ['device', 'telnet', 'ssh' , 'location']

		device = forms.CharField(label="device", max_length=100, required=True)
		telnet = forms.CharField(label="telnet_connection", max_length=100, required=True)
		ssh = forms.CharField(label="ssh_connection", max_length=100, required=True)

		OPTIONS = [
		('sjc15', 'sjc15'),
		('sjc16', 'sjc16'),
		('ful', 'ful'),
		]
		location = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))


class MyUpdateTestbed(forms.Form):
	device = forms.CharField(label="device", widget=forms.Textarea(attrs={'class': 'fieldWrapper'}), max_length=100,)
	telnet = forms.CharField(label="telnet", widget=forms.Textarea(attrs={'class': 'fieldWrapper'}), max_length=100,)
	ssh = forms.CharField(label="ssh", widget=forms.Textarea(attrs={'class': 'fieldWrapper'}), max_length=100)
	notes = forms.CharField(label="notes", widget=forms.Textarea(attrs={'class': 'fieldWrapper'}))
	device_type = forms.CharField(label="device_type", widget=forms.Textarea(attrs={'class': 'fieldWrapper'}), max_length=100)

	OPTIONS = [
	('sjc15', 'sjc15'),
	('sjc16', 'sjc16'),
	('ful', 'ful'),
	]
	location = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))

	OPTIONS = [
	('notfree', 'In Use'),
	('free', 'Not In Use')	
	]
	usage = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))

	OPTIONS = [
	('ftd', 'FTD'),
	('fmc', 'FMC'),
	('router', 'Router'),
	('switch', 'Switch')
	]
	device_type = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))



	class Meta:
	
		model = Testbed
		fields = ('device', 'telnet', 'ssh' , 'location', 'notes', 'usage', 'device_type')



class ExcelForm(forms.Form):
    generate_excel = forms.BooleanField(required=False, widget=forms.HiddenInput())
