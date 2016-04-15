import os
from .reddit_models import Reddit
from runt.models import Settings
from runt.utilities.base_extension import BaseExtension

class Extension(BaseExtension):
		
	def inject_variables(self, **kwargs):
		import praw
		r = praw.Reddit(user_agent="Test Script")

		sp = Settings().select().where(Settings.field == 'reddit_api--show_posts')
		limit = sp.get().value if sp.exists() else 5


		submissions = r.get_subreddit('python').get_hot(limit=int(limit))
		
		add_on = {}

		for s in submissions:
			add_on[s.id] = {
				"url": s.url,
				"title": s.title
			}
		
		if kwargs:
			kwargs['reddit_api'] = add_on
			return kwargs
		
		return add_on

	def install_scripts(self):
		os.system('pip3 install praw')
		return

	def install_models(self):
		return [Reddit]