import config, os, json
from flask import render_template, request, redirect, url_for
from runt.models import *
from playhouse import shortcuts
from werkzeug import secure_filename

_theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value

def all():

	object_type = request.args.get('object-type') or 'page'
	pageheader = object_type.title() + ' Pages' if object_type != 'page' else 'Pages'

	pages = Pages.select().where(Pages.object_type == object_type).order_by(+Pages.title)

	return render_template("admin-all-pages.html", pages=pages, object_type=object_type, pageheader=pageheader)

def add():

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

			for name, file in request.files.items():
				if name.startswith("field--"):
					name_split = name.split("--")
					field_type = name_split[1]
					field_id = name_split[2]
					if field_type == 'photo':

						if file: # and file.filename.endswith(('.jpg','.png')):
							filename = secure_filename(file.filename)
							file.save(os.path.join(config.RUNT_UPLOADS, filename))
							print(os.path.join(config.RUNT_UPLOADS, filename))
					
						f = Fields(page_id=p.id, field_id=field_id, field_value=filename)
						f.save()

			return redirect(url_for('admin_edit_pages', id=p.id))
	
	fields = _object_fields(object_type) or None
	
	return render_template("admin-add-page.html", error=err_return, object_type=object_type, fields=fields)

def edit(id):

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
		fields = _object_fields(object_type) or None

		allf = Fields.select().where(Fields.page_id == id)
		
		for a in allf:
			#print(shortcuts.model_to_dict(a))
			fields[a.field_id]['value'] = a.field_value


		return render_template("admin-edit-page.html", values=values,\
									error=err_return, object_type=object_type,\
									fields=fields)

	return '404 page'

def _object_fields(obj):

	fields = {}

	objects_json = config.ROOT_DIR + '/themes/' + _theme + '/objects.json'
	
	if os.path.exists(objects_json):
		
		with open(objects_json, "r") as oj:
		
			_o_decode = json.loads(oj.read())

			fields = _o_decode[obj]['fields'] 	

		return fields

	return False