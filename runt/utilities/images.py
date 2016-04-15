import os
import json
import config
from ..models import Settings
from PIL import Image, ImageOps

class Images():
	def __init__(self):
		self.theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
		self.image_sizes = self._image_size_list()

	def _image_size_list(self):
		_image_sizes = {
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

		theme_json_path = config.ROOT_DIR + '/themes/' + self.theme + '/theme.json'

		if os.path.exists(theme_json_path):
			with open(theme_json_path, 'r') as _tj:
				_t_decode = json.loads(_tj.read())
				if 'image_sizes' in _t_decode:
					_image_sizes.update(_t_decode['image_sizes'])

		return _image_sizes

	def upload_processing(self, path, filename):
		"""
		Crops images based on theme.json's image_sizes object. The values in 
		theme.json will override the defaults if they are provided.
		"""

		file, file_ext = os.path.splitext(filename)	

		for _is_id, _is_details in self.image_sizes.items():
			"""
			redeclare this everytime so the same origin file is being used
			"""
			im = Image.open(os.path.join(path, filename))

			print(_is_details)

			size = (int(_is_details['width']), int(_is_details['height']))
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
					im = im.resize(size, Image.ANTIALIAS)
			elif _is_details['crop'] == 'soft':	
				im.thumbnail(size, Image.ANTIALIAS)

			im.save(path + '/' + file + '.' + _is_id + file_ext, quality=100, subsampling=0)

		return

	def get_image(self, url, size):
		
		file, file_ext = os.path.splitext(url)

		final_image = file + '.' + size + file_ext

		return final_image
