import os
from runt.base_extension import BaseExtension

class Extension(BaseExtension):
		
	def inject_variables(self, **kwargs):
		import praw
		r = praw.Reddit(user_agent="Test Script")
		submissions = r.get_subreddit('python').get_hot(limit=5)
		
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

	def install(self):
		os.system('pip3 install praw')
		return