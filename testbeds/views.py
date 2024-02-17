from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django.contrib import messages
from django.views import View

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Testbed
from .forms import MyUpdateTestbed, ExcelForm
from .filters import YourModelFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from openpyxl import Workbook
from django.http import HttpResponse
from .constants import users, send_webex_message
import datetime
from django.utils import timezone



button_submited ={'Submitted': False}
 
location_dict = {'sjc15': 'San Jose Building 15',
	'sjc16': 'San Jose Building 16',
	'ful': 'Fulton'}

device_type_dict = {'all': 'All',
					'ftd': 'FTD',
					'fmc': 'FMC',
					'router': 'Router',
					'switch': 'Switch'}

date_dict = {'latest': ('Latest', "Latest"),
			'oldest': ('Oldest', "Oldest")}

usage_dict = {'all': ('All', "all", "All Devices"),
			'not_used': ('Unused', "free", "Unused Devices"),
			'used': ('Used', "notfree", "Used Devices")}

@method_decorator(login_required, name='dispatch')
class TestbedListView(ListView):
	model = Testbed
	template_name = 'testbed-home.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'testbeds'
	context = {'title': 'Devices Home'}

	def get(self, request):
		generate_excel = self.request.GET.get('generate_excel')
		if generate_excel:
			wb = Workbook()
			ws = wb.active
			headers = ['Username','Location','Device','Usage','Date','Type','Telnet','SSH','Notes']
			ws.append(headers)
			objs = Testbed.objects.all()
			for data in objs:
				username = str(data.testbed_uploader)
				row_data = [str(data.testbed_uploader),data.location,data.device,data.usage,str(data.date_posted),data.device_type,data.telnet,data.ssh,data.notes]
				ws.append(row_data)
				
			response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
			response['Content-Disposition'] = 'attachment; filename=my_excel_file.xlsx'
			wb.save(response)
			return response
		return render(request, self.template_name, {'title': 'Devices Home'})

	


@method_decorator(login_required, name='dispatch')
class TestbedDetailListView(ListView):
	model = Testbed
	template_name = 'location-detail.html'
	context_object_name = 'devices'

	def get_context_data(self):
		location = self.kwargs.get('parameter')  # Get the category parameter from URL
		selected_date = self.request.GET.get('date','oldest') 
		selected_usage = self.request.GET.get('usage','all')
		selected_user = self.request.GET.get('user','all')
		selected_device_type = self.request.GET.get('device_type','all')
		searched_device = self.request.GET.get('search_device','')
		submitted_button = self.request.GET.get('submitted_button')

		order_by = "date_posted"

		if submitted_button == "Submit":
			submitted_button = "Reset-and-Submit"
		else:
			submitted_button = 'Submit'
			searched_device = ""

		temp_usage = usage_dict[selected_usage]
		temp_date = date_dict[selected_date]
		temp_device_type = device_type_dict[selected_device_type]

		device_objects = Testbed.objects.filter(location=location)
		if searched_device:
			device_objects = device_objects.filter(device=searched_device)
		all_users = User.objects.all()
		if device_objects:
			order_by_message_str = "Filter Date: Oldest"
			if 'latest' in selected_date:
				order_by = "-date_posted"
				order_by_message_str = "Filter Date: Latest"

			if selected_usage != "all":
				 device_objects = device_objects.filter(usage=temp_usage[1])

			username = "All"
			if selected_user != "all":
				device_objects = device_objects.filter(testbed_uploader=selected_user)
				username = User.objects.filter(id=selected_user)[0].username
			# device_type = "All"
			if selected_device_type != "all":
				device_objects = device_objects.filter(device_type=selected_device_type)
				device_type = device_type_dict[selected_device_type]
			messages.success(self.request, f'Filter Date: {temp_date[1]}, Filter Usage: {temp_usage[2]}, Filter User: {username}, Filter User: {temp_device_type}')  
			paginator = Paginator(device_objects.order_by(order_by), per_page=5)
			page_number = self.request.GET.get('page',1)
			page_obj = paginator.get_page(page_number)

			context = {'devices': paginator.page(int(page_number)), "is_paginated":True, 'page_obj': page_obj, "location": location_dict[location], 
			'date': selected_date, 'usage': selected_usage, 'all_users': all_users, 'selected_date': temp_date[0], 'selected_usage': temp_usage[0], 
			'selected_user': username, 'selected_device_type': temp_device_type, 'searched_device': searched_device, 'submit_button_name': submitted_button,
			'title': f'Devices:- {location_dict[location]}'}
			return context
		else:
			paginator = Paginator(device_objects.order_by(order_by), per_page=5)
			page_number = self.request.GET.get('page',1)
			page_obj = paginator.get_page(page_number)
			messages.error(self.request, f'Device {searched_device} does not exist')  
			return {'devices': paginator.page(int(page_number)),'submit_button_name': submitted_button}

	def post(self, request, *args, **kwargs):
		pk = self.request.POST.get('pk_val')
		location = self.kwargs.get('parameter')
		obj = get_object_or_404(Testbed,pk=pk)
		testbed_uploader = obj.testbed_uploader.username
		device = obj.device
		user = request.user.username
		if request.method == 'POST':
			send_webex_message(False,testbed_uploader,device,sending_user=user)
			return redirect('location-detail', location)


@method_decorator(login_required, name='dispatch')
class PostTestbed(CreateView):
	template_name = 'testbeds/testbed_form.html' 

	def get(self, request, *args, **kwargs):
		form = MyUpdateTestbed()
		return render(request, self.template_name)


	def post(self, request, *args, **kwargs):
		form = MyUpdateTestbed(request.POST)
		if form.is_valid():
			context = {'form': form}
			device = request.POST.get('device', '')
			telnet = request.POST.get('telnet', '')
			ssh = request.POST.get('ssh', '')
			location = request.POST.get('location', '')
			notes = request.POST.get('notes')
			usage = request.POST.get('usage','')
			device_type = request.POST.get('device_type','')
			user = request.user

			existing_device = Testbed.objects.filter(device=device)
			existing_telnet = Testbed.objects.filter(telnet=telnet)
			existing_ssh = Testbed.objects.filter(ssh=ssh)

			if existing_device.exists() and existing_device[0].location == location:
				messages.error(request, f'Name already exists in {location}')
				return render(request, self.template_name, {'context': context})
			elif existing_telnet.exists():
				messages.error(request, f'Telnet Connection Entered already exists in {location_dict[existing_telnet[0].location]} for device {existing_telnet[0].device}')
				return render(request, self.template_name, {'context': context})
			elif Testbed.objects.filter(ssh=ssh).exists():
				messages.error(request, f'SSH Connection details already exists in {location_dict[existing_ssh[0].location]}  for device {existing_ssh[0].device}')
				return render(request, self.template_name, {'context': context})
			else:
				testbed = Testbed(device=device,
								ssh=ssh,
								telnet=telnet,
								location=location,
								notes=notes,
								usage=usage,
								device_type=device_type,
								testbed_uploader=user)
				testbed.save()
				messages.success(request, f'Testbed {device} Details Uploaded Succesfully!')  # Set success message
				return render(request, "testbeds/testbed-home.html", {"context": context})

@method_decorator(login_required, name='dispatch')
class TestbedUpdateView(View):
	model = Testbed
	template_name = 'testbeds/testbed-detail.html'
	
	def get(self, request, pk):

		obj = get_object_or_404(Testbed, pk=pk)
		form = MyUpdateTestbed(initial={'device': obj.device, 'location': obj.location, 'telnet': obj.telnet, 
										'ssh': obj.ssh, 'notes': obj.notes, 'usage': obj.usage, 'device_type': obj.device_type})
		return render(request, self.template_name, {'form': form, 'object': obj})

	def check_existing_object(self,existing_obj,current_pk):
		if existing_obj:
			if len(existing_obj) == 1:
				existing_pk = existing_obj[0].pk
				return (existing_pk != current_pk, existing_pk)
		return (False, None)
					

	def post(self, request, pk, *args, **kwargs):
		obj = get_object_or_404(Testbed, pk=pk)
		form = MyUpdateTestbed(request.POST)
		if form.is_valid():
			context = {'form': form}
			device = form.cleaned_data['device']
			location = form.cleaned_data['location']
			telnet = form.cleaned_data['telnet']
			ssh = form.cleaned_data['ssh']
			notes = form.cleaned_data['notes']
			usage = form.cleaned_data['usage']
			device_type = form.cleaned_data['device_type']

			obj.device = device
			obj.location = location
			obj.telnet = telnet
			obj.ssh = ssh
			obj.notes = notes
			obj.usage = usage
			obj.device_type = device_type
			obj.testbed_uploader = request.user
			# obj.date_posted = datetime.datetime.now(timezone.utc)

			existing_telnet_obj = Testbed.objects.filter(telnet=telnet)
			existing_ssh_obj = Testbed.objects.filter(ssh=ssh)
			existing_device_obj = Testbed.objects.filter(location=location,device=device)

			if existing_device_obj and existing_device_obj[0].pk != pk:
				messages.error(request, f'This Name already exists in {location_dict[location]}. Please use a different name')
				return render(request, "testbeds/testbed-detail.html", {'form': form, 'object': obj})

			if existing_telnet_obj and existing_telnet_obj[0].pk != pk:
				messages.error(request, f'Telnet Details already exists for {existing_telnet_obj[0].device} in {d[existing_telnet_obj[0].location]}')
				return render(request, "testbeds/testbed-detail.html", {'form': form, 'object': obj})

			if existing_ssh_obj and existing_ssh_obj[0].pk != pk:
				messages.error(request, f'SSH Details already exists for {existing_ssh_obj[0].device} in {d[location]}')
				return render(request, "testbeds/testbed-detail.html", {'form': form, 'object': obj})

			obj.save()
			messages.success(request, f'Update Succesful!')  # Set success message
			return redirect('location-detail', location)

class TestbedDeleteView(View):
	template_name = 'testbeds/testbed-delete.html'

	def get(self, request, pk):
        # Get the object you want to delete
		obj = get_object_or_404(Testbed, pk=pk)

		context = {
        	'object': obj,
		}

		return render(request, self.template_name, context)

	def post(self, request, pk):

		obj = get_object_or_404(Testbed, pk=pk)
		location = obj.location
		if not request.user.is_superuser:
			messages.error(request, 'You do not have Permission to Delete Devices')
			return redirect('location-detail', location)

		obj.delete()
		return redirect('location-detail', location)





		