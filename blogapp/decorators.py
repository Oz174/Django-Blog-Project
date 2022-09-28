from django.shortcuts import render , redirect
from django.http import HttpResponse


def user_unauthorized(view_function):
	def wrapper_func(request, *args , **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_function(request, *args, **kwargs) 
	return wrapper_func

def only_admins(view_function):
	def wrapper_func(request, *args , **kwargs):
		if not (request.user.is_superuser or request.user.is_staff):
			return HttpResponse("Not Authorized to view")
		else:
			return view_function(request, *args, **kwargs) 
	return wrapper_func
