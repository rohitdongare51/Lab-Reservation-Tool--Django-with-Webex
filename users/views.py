from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
	if request.method == "POST":
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account Created!')
				return redirect('login')
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
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		is_post_request = False
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {'u_form': u_form,
			   'p_form': p_form}
	return render(request, 'users/profile.html', context)



# def your_view(request):
#     # Filter the queryset based on the condition (field2 > 100)
#     filtered_queryset = Profile.objects.filter(user=100)

#     # Get values for field1 and field2 from the filtered queryset
#     values_list = filtered_queryset.values('field1', 'field2')

#     # Pass the values_list to the template or use it as needed
#     return render(request, 'your_template.html', {'values_list': values_list})