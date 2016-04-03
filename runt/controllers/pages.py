import config, os, json
import datetime
from PIL import Image, ImageOps
from flask import render_template, request, redirect, url_for
from runt.models import *
from runt.utils import noindex
from playhouse import shortcuts
from werkzeug import secure_filename

class PageController():
	def __init__(self):
		self._theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value

	@noindex
	def all(self):

		object_type = request.args.get('object-type') or 'page'
		pageheader = object_type.title() + ' Pages' if object_type != 'page' else 'Pages'

		pages = Pages.select().where(Pages.object_type == object_type).order_by(+Pages.title)

		return render_template("all-pages.html", pages=pages, object_type=object_type, pageheader=pageheader)

	@noindex
	def add(self):

		object_type = request.args.get('object-type') or 'page'

		err_return = {}
		if request.method == 'POST':
			if not request.form['title']:
				err_return['title'] = "Title is required"
			if not request.form['slug']:
				err_return['slug'] = "Slug is required"
			if not request.form['content']:
				err_return['content'] = "Content is required"
			if not err_return:
				
				p = Pages(title=request.form['title'], slug=request.form['slug'], \
					content=request.form['content'], object_type=object_type)
				p.save()

				for name, v in request.form.items():
					if name.startswith("field--"):
						name_split = name.split("--")
						field_type = name_split[1]
						field_id = name_split[2]

						if v:
							f = Fields(page_id=p.id, field_id=field_id, field_value=v)
							f.save()


				n = datetime.date.today()
				year_dir = str(n.year)
				year_path = config.RUNT_UPLOADS + year_dir
				month_dir = '/' + str(format(n.month, '02d'))
				month_path = year_path + month_dir
				relative_path = '/uploads/' + year_dir + month_dir + '/'

				for name, file in request.files.items():
					if name.startswith("field--"):
						name_split = name.split("--")
						field_type = name_split[1]
						field_id = name_split[2]
						
						if field_type == 'photo':

							if file and file.filename.endswith(('.jpg','.png')):
								
								if not os.path.exists(year_path):
									os.mkdir(year_path)

								if not os.path.exists(month_path):
									os.mkdir(month_path)

								filename = secure_filename(file.filename)

								file.save(os.path.join(month_path, filename))

								self._image_processing(month_path, filename)

								field_out = relative_path + filename

							else:

								field_out = file
								
						
							f = Fields(page_id=p.id, field_id=field_id,\
										field_value=field_out)
							f.save()

				return redirect(url_for('admin.edit_pages', id=p.id))
		
		fields = self._object_fields(object_type) or None

		pageheader = "Add New " + object_type.title()
		
		return render_template("add-page.html", error=err_return,\
								 object_type=object_type, fields=fields,\
								 pageheader=pageheader)

	@noindex
	def edit(self, id):

		err_return = {}
		p = Pages.select().where(Pages.id == id)

		if p.exists():
			values = p.get()

			if request.method == 'POST':
				if not request.form['title']:
					err_return['title'] = "Title is required"
				if not request.form['slug']:
					err_return['slug'] = "Slug is required"
				if not request.form['content']:
					err_return['content'] = "Content is required"
				if not err_return:
					p_update = Pages.update(title=request.form['title'], slug=request.form['slug'], \
						content=request.form['content']).where(Pages.id == id).execute()
					values = {}
					values['title'] = request.form['title']
					values['slug'] = request.form['slug']
					values['content'] = request.form['content']
					values['id'] = id

			object_type = p.get().object_type
			fields = self._object_fields(object_type) or None

			allf = Fields.select().where(Fields.page_id == id)
			
			for a in allf:
				fields[a.field_id]['value'] = a.field_value


			return render_template("edit-page.html", values=values,\
										error=err_return, object_type=object_type,\
										fields=fields)

		return '404 page'

	def _object_fields(self, obj):

		fields = {}

		objects_json = config.ROOT_DIR + '/themes/' + self._theme + '/objects.json'
		
		if os.path.exists(objects_json):
			
			with open(objects_json, "r") as oj:
			
				""" BROKEN FOR PAGES """

				_o_decode = json.loads(oj.read())

				if obj in _o_decode and 'fields' in _o_decode[obj]:
					
					fields = _o_decode[obj]['fields']
					
					for _k, _v in fields.items():
						
						if _v['type'] == 'cross_object' and 'object' in _v:
						
							_p_o = Pages.select().where(Pages.object_type == _v['object'])
							
							_temp_o = {}

							for _p in _p_o:
						
								_temp_o[_p.id] = _p.title

							fields[_k]['object_items'] = _temp_o

			return fields

		return False

	def _image_processing(self, path, filename):
		"""
		Crops images based on theme.json's image_sizes object. The values in 
		theme.json will override the defaults if they are provided.
		"""

		image_sizes = {
			"large": {
				"crop": "soft",
				"width": "1000",
				"height": "1000"
			},
			"medium": {
				"crop": "soft",
				"width": "500",
				"height": "500"
			},
			"small": {
				"crop": "hard",
				"width": "200",
				"height": "200"
			}
		}

		theme_json_path = config.ROOT_DIR + '/themes/' + self._theme + '/theme.json'

		with open(theme_json_path, 'r') as _tj:
			_t_decode = json.loads(_tj.read())
			image_sizes.update(_t_decode['image_sizes'])

		print(image_sizes)

		file, file_ext = os.path.splitext(filename)

		for _is_id, _is_details in image_sizes.items():

			size = (int(_is_details['width']), int(_is_details['height']))

			im = Image.open(os.path.join(path, filename))
			image_ratio = im.size[0] / im.size[1]
			ratio = size[0] / size[1]

			if _is_details['crop'] == 'hard':
				if ratio > image_ratio:
					im = im.resize((size[0], size[0] * im.size[1] // im.size[0]), Image.ANTIALIAS)
					box = (0, ((im.size[1] - size[1]) // 2), im.size[0], (im.size[1] + size[1]) // 2)
					im = im.crop(box)
				elif ratio < image_ratio:
					im = im.resize(((size[1] * im.size[0]) // im.size[1], size[0]), Image.ANTIALIAS)
					box = ((im.size[0] - size[0]) // 2, 0, (im.size[0] + size[0]) // 2, im.size[1])
					im = im.crop(box)
				else:
					im = im.resize(size)
			elif _is_details['crop'] == 'soft':	
				im.thumbnail(size)

			im.save(path + '/' + file + '.' + _is_id + '.' + file_ext, quality=100, subsampling=0)

		return

