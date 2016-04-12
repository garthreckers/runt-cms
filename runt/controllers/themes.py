import os, json
import config
from peewee import *
from runt.utils import noindex
from playhouse import shortcuts
from runt.models import *
from flask import send_from_directory, redirect
from runt.extensions import load_template
from ..models import Fields

class ThemeController():
	def __init__(self):
		self._theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
		self._theme_dir = config.ROOT_DIR + '/themes/' + self._theme + '/'

	def index(self):
		content = self._theme_json_objects('index')

		return load_template('index.html', content=content)

	def pages(self, slug):
		json_content = self._theme_json_objects('page')
		if not json_content:
			content = Pages.select().where(Pages.slug == slug, Pages.object_type == 'page').get()
			content = shortcuts.model_to_dict(content)
		else:
			content = json_content

		return load_template('page.html', content=content)

	def object_pages(self, obj, slug):
		if obj == "page":
			return redirect('/' + slug)

		json_content = self._theme_json_objects(obj)
		if not json_content:
			content = Pages.select().where(Pages.slug == slug, Pages.object_type == obj).get()
			content = shortcuts.model_to_dict(content)
		else:
			content = json_content

		template_set = ['page-' + str(obj) + '.html', 'page.html']

		for tn in template_set:

			if os.path.exists(config.ROOT_DIR + '/themes/' + self._theme + '/' + tn):

				return load_template(tn, content=content)

		return '404'

	def get_field(self, id, field_id):

		fields = Fields().select().where((Fields.page_id == id) & (Fields.field_id == field_id))

		if fields.exists():
			field_value = ""
			if fields.get().field_type == 'photo':
				home_url = Settings.select(Settings.value).where(Settings.field == 'homepage').get().value
				field_value += home_url
			field_value += fields.get().field_value
			return field_value

		return False


	def global_variables(self):
		template_json = self._theme_dir + 'theme.json'

		if os.path.exists(template_json):

			_t_decode = None

			with open(template_json, "r") as tj:
			
				_t_decode = json.loads(tj.read())

			return {"global": _t_decode['globals']}

		return False


	def _theme_json_objects(self, template_name):

		content = {}

		template_json = self._theme_dir + template_name + '.json'
		
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