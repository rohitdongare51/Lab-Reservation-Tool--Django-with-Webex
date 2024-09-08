from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .constants import send_webex_message
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
import time

allowed_users = ['user1','user2', 'user3', 'user4', 'user5','user6','user7'], 
user_dict = {'user1': (0,'test_password'), 'user2': (0, 'test'), 'user3': (0, 'test'), 'user4': (0, 'test'), 'user5': (0, 'test'), 'user6': (0, 'test'), 'user7': (0, 'test'), 'user8': (0, 'test')}
time_dict = {'start_time': time.time()}
def register(request):
	if request.method == "POST":
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				if username in allowed_users:
					form.save()
					messages.success(request, f'Account Created!')
					return redirect('login')
				else:
					messages.error(request,f'{username} is not a valid Username! Please use your cec username')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		is_post_request = True
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
									request.FILES,
									instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			username = u_form.cleaned_data.get('username')
			if username in allowed_users:
				u_form.save()
				p_form.save()
				messages.success(request, f'Your account has been updated!')
				return redirect('profile')
			else:
				messages.error(request, f'{username} is not a valid Username! Please use your cec username')
				return redirect('profile')
	else:
		is_post_request = False
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {'u_form': u_form,
			   'p_form': p_form}
	return render(request, 'users/profile.html', context)


class ResetPasswordView(UpdateView):
	model = Profile
	template = 'password_reset.html'

	def get(self,request):
		return render(request, self.template_name)
	
	def post(self, request, *args, **kwargs):
		username = self.request.POST.get('username')
		password = self.request.POST.get('password')
		code = send_webex_message(username)
		user_dict[username] = (code,password)
		time_dict['start_time'] = time.time()
		return render(request, 'users/password_reset_done.html')

class ResetPasswordConfirmView(UpdateView):
	model = Profile
	# template = 'password_reset_confirm.html'


	def get(self,request):
		return render(request, self.template_name)
	
	def post(self, request, *args, **kwargs):
		username = self.request.POST.get('username')
		code = self.request.POST.get('code')
		if username and time.time()-time_dict['start_time'] < 60:
			if code == user_dict[username][0]:
				u = User.objects.get(username=username)
				u.set_password(user_dict[username][1])
				u.save()
				user_dict[username] = (0,'test')
				return render(request, 'users/password_reset_complete.html')
			messages.error(self.request, f'Codes provided do not match')  
		messages.error(self.request, f'You did not enter code within 1 minute')  
		return render(request, 'users/password_reset_incomplete.html')

	
