import config, os, json
import datetime
from ..images import Images
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
							f = Fields(page_id=p.id, field_id=field_id, field_value=v, field_type=field_type)
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

								Images().upload_processing(month_path, filename)

								field_out = relative_path + filename

							else:

								field_out = file
								
						
							f = Fields(page_id=p.id, field_id=field_id,\
										field_value=field_out, field_type=field_type)
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
					p_update = Pages().update(title=request.form['title'], slug=request.form['slug'], \
						content=request.form['content']).where(Pages.id == id).execute()
					values = {}
					values['title'] = request.form['title']
					values['slug'] = request.form['slug']
					values['content'] = request.form['content']
					values['id'] = id

					for name, v in request.form.items():
						if name.startswith("field--"):
							name_split = name.split("--")
							field_type = name_split[1]
							field_id = name_split[2]

							if v and Fields().select().where(
										(Fields.page_id == id) & (Fields.field_id == field_id)
									).exists():
								f_update = Fields().update(field_value=v).where(
												(Fields.page_id == id) & (Fields.field_id == field_id)
											).execute()
							else:
								f = Fields(page_id=id, field_id=field_id, field_value=v, field_type=field_type)
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

									Images().upload_processing(month_path, filename)

									field_out = relative_path + filename

								else:

									field_out = file
									
								if Fields().select().where(
										(Fields.page_id == id) & (Fields.field_id == field_id)
									).exists():

									f_update = Fields().update(field_value=field_out).where(
												(Fields.page_id == id) & (Fields.field_id == field_id)
											).execute()

								else:

									f = Fields(page_id=id, field_id=field_id,\
												field_value=field_out, field_type=field_type)
									f.save()

					return redirect(url_for('admin.edit_pages', id=id))

			object_type = p.get().object_type
			fields = self._object_fields(object_type) or None

			allf = Fields.select().where(Fields.page_id == id)
			
			for a in allf:
				if a.field_value:
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

	

