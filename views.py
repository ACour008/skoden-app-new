import os
import os.path as op
import datetime

import soundcloud

from extensions import cache, db

from models import Role, User, Article, Author, Tag, SKNTextAreaField, \
SKNAdvancedTagField, STATUS
import skoden_helpers as h

from flask import Blueprint, send_file, request, jsonify, redirect, url_for, abort
from flask import current_app as app

from flask_admin import Admin, AdminIndexView, form, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.menu import MenuLink

from sqlalchemy.event import listens_for
from jinja2 import Markup
from wtforms import validators as v
from flask_security import current_user

views = Blueprint(
	'views',
	__name__,
	static_folder='static',
	template_folder='templates'
)


# URL VIEWS
@views.route('/', methods=['GET', 'POST'])
def index():
	return send_file("templates/layout.html")


@views.route('/api/get-sc-data', methods=['GET'])
def get_sc_data():
	obj = {}
	client = soundcloud.Client(client_id=app.config['SOUNDCLOUD_CLIENT_KEY'])
	oembed = client.get('/oembed', url="http://soundcloud.com/the-skoden-chronicles/tracks")

	playlists = client.get('/users/%s/playlists' % (app.config['SOUNDCLOUD_USER_ID']))
	tracks = client.get('users/%s/tracks' % (app.config['SOUNDCLOUD_USER_ID']))

	obj['about'] = h.makehtml(oembed.obj['description'])
	obj['playerHtml'] = oembed.obj['html']
	obj['allPlaylists'] = playlists.raw_data
	obj['allTracks'] = tracks.raw_data

	return jsonify(obj), 200


@views.route('/api/entries', methods=['GET', 'POST'])
def entries():
	pass


@views.route('/api/entries/<id>', methods=['GET', 'PUT', 'DELETE'])
def entry_id():
	pass



# ADMIN VIEWS

class SKNBaseModelView(ModelView):

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			# Will not show up on menu on Admin page
			return False
		if current_user.has_role('superuser'):
			return True
		return False

	def _handle_view(self, name, **kwargs):
		"""
		Override builtin _handle_view in order to redirect users when a view is
		not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				abort(403)
			else:
				# login
				return redirect(url_for('security.login', next=request.url))


class ArticleView(SKNBaseModelView):
	"""
	Creates the Admin view page for all Articles
	"""
	
	form_overrides = dict(body=SKNTextAreaField)
	create_template = 'admin/create.html'
	edit_template = 'admin/edit.html'
	column_list = ('title', 'author', 'status', 'tag', 'date_published', 'last_edited')
	form_choices = {'status': STATUS }
	form_create_rules = (rules.Header('New Article'),
		'title', 'body', 'author', 'tagfield', 'status')
	form_edit_rules = (rules.Header('Edit Article'), 
		'title', 'permalink', 'body', 'author', 'tagfield', 'status')
	column_sortable_list = ('title', 
		('author', 'author.last_name'), 
		'status', ('tag', 'tag.name'), 'date_published', 'last_edited')
	form_extra_fields = { 'tagfield': SKNAdvancedTagField('Tags') }
	column_formatters = dict(status=lambda v, c, m, p: m.status.value)

	def on_form_prefill(self, form, id):
		article = Article.query.get(id)
		form.tagfield.object_data = article.tag
		print(article.status.code)
		form.status.process_data(article.status.code)
		#form.status = article.status

	def on_model_change(self, form, model, is_created):
		if not is_created:
			print("We gonna edit things!")

	def create_model(self, form):
		article = Article(
			title=form.title.data,
			permalink=h.slugify(form.title.data),
			date_published=datetime.datetime.utcnow(),
			last_edited=datetime.datetime.utcnow(),
			# status=STATUS[1][1],
			body=form.body.data,
			author_id = form.author.data.id,
			status=form.status.data
		)
		for tag in form.tagfield.data:
			article.tag.append(tag)

		db.session.add(article)
		db.session.commit()
		return redirect(self.get_save_return_url(Article))

class AuthorView(SKNBaseModelView):
	"""
	Creates the Admin view page for Authors
	"""
	pass

class TagView(SKNBaseModelView):
	"""
	Creates the Admin view page for Tag model
	"""
	pass

class MyAdminView(AdminIndexView):
	"""
	Creates the Index page for the entire Admin backend
	"""
	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			# Will not show up on menu on Admin page
			return False
		if current_user.has_role('superuser'):
			return True
		return False

	def _handle_view(self, name, **kwargs):
		"""
		Override builtin _handle_view in order to redirect users when a view is
		not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				abort(403)
			else:
				# login
				return redirect(url_for('security.login', next=request.url))
	
	@expose('/')	
	def index(self):
		"""
		Main function for view
		"""
		return self.render("admin/index.html")


class AdminMenuLink(MenuLink):
	"""
	Created so Admin Menu Link disappears when user is not logged in.
	"""
	def is_visible(self):
		if not current_user.is_active and not current_user.is_authenticated:
			return False
		if current_user.has_role('superuser'):
			return True
		return False