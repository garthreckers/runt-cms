import os, json
import config
from peewee import *
from playhouse import shortcuts
from runt.models import *
from flask import send_from_directory, redirect
from runt.extensions import load_template

_theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value

def static(filename):
	static_path = config.ROOT_DIR + '/themes/' + _theme + '/static'
	return send_from_directory(static_path, filename)


def index():
	content = _theme_json_objects('index')
	template_name = _theme + '/index.html'

	return load_template(template_name, content=content)

def pages(slug):
	json_content = _theme_json_objects('page')
	if not json_content:
		content = Pages.select().where(Pages.slug == slug, Pages.object_type == 'page').get()
		content = shortcuts.model_to_dict(content)
	else:
		content = json_content

	template_name = _theme + '/page.html'
	return load_template(template_name, content=content)

def object_pages(obj, slug):
	if obj == "page":
		return redirect('/' + slug)

	json_content = _theme_json_objects(obj)
	if not json_content:
		content = Pages.select().where(Pages.slug == slug, Pages.object_type == obj).get()
		content = shortcuts.model_to_dict(content)
	else:
		content = json_content

	template_set = ['page-' + str(obj) + '.html', 'page.html']

	for tn in template_set:

		if os.path.exists(config.ROOT_DIR + '/themes/' + _theme + '/' + tn):

			template_name = _theme + '/' + tn
			return load_template(template_name, content=content)

	return '404'

def _theme_json_objects(template_name):

	content = {}

	template_json = config.ROOT_DIR + '/themes/' + _theme + '/' + template_name + '.json'
	
	if os.path.exists(template_json):
		
		with open(template_json, "r") as tj:
		
			_t_decode = json.loads(tj.read())

			for k, v in _t_decode['objects'].items():
				
				_p_obj = None
				
				if v['fields'] == "*":
				
					_p_obj = (Pages
								.select()
								.where(Pages.object_type == k))

				if type(v['fields']) is dict:
				
					_objs = []
				
					for inner_k, inner_v in v['fields'].items():
						
						_objs.append(inner_v)

					_p_obj = (Pages
								.select(*[getattr(Pages, a) for a in _objs])
								.where(Pages.object_type == k))

				if 'limit' in v:
					_p_obj = _p_obj.limit(v['limit'])
				
				else:
					_p_obj = _p_obj.limit(10)
				
				_p_content = []
				
				for _p_dict in _p_obj.dicts():
					_p_content.append(_p_dict)
				
				content[k] = _p_content
		
		return content

	return False