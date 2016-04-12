from functools import wraps
from flask import make_response

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

