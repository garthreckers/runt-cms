"""
Group of functions to keep make 
some auth code easier
"""
from functools import wraps
from flask import redirect, url_for, make_response
from ..admin.install import runt_installed

def login_checker(func):
	"""
	Decorator to be used with Controllers to check if
	user is logged in and redirect to login page if not
	"""
	@wraps(func)
	def func_wrap(*args, **kwargs):
		if not runt_installed():
			return redirect(url_for('admin.install'))

		if logged_in():
			return func(*args, **kwargs)
		else:
			return redirect(url_for('admin.login'))
	return func_wrap

def add_response_headers(headers={}):
	def decorator(func):
		@wraps(func)
		def decorator_function(*args, **kwargs):
			resp = make_response(func(*args, **kwargs))
			h = resp.headers
			for header, value in headers.items():
				h[header] = value
			return resp
		return decorator_function
	return decorator

def noindex(func):
	return add_response_headers({"X-Robot-Tag": "noindex nofollow"})(func)