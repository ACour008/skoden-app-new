from flask import Flask, url_for
from flask_wtf.csrf import CSRFProtect

from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail

from flask_admin import Admin
from flask_admin import helpers as admin_helpers

import skoden_helpers as h
import models
from extensions import db, cache
from views import views, MyAdminView, ArticleView, AuthorView, AdminMenuLink, \
TagView

import soundcloud
import urllib
import sys


# Set up app, bring in config file, instantiate flask_mail
def create_app(config_file='config.cfg'):
	"""
	For setup purposes
	"""
	app = Flask(__name__)
	app.config.from_pyfile(config_file)
	app.register_blueprint(views)
	CSRFProtect(app)
	return app

def register_extensions(app, data=False):
	"""
	Registers extensions to be used within the app context
	The list of apps:
	    db - database used for site articles
	    cache - to speed up loadtimes for larger resources
	    mail - for contact form
	    security - used to login editors
	    admin - gives editors a backend to publish, edit articles
	""" 
	db.init_app(app)
	cache.init_app(app)
	mail = Mail(app)

	# Security setup
	user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
	security = Security(app, user_datastore)

	# Admin backend
	admin = Admin(
		app,
		index_view=MyAdminView(name="Admin Home", category="Admin"),
		name="Skoden Chronicles",
		template_mode='bootstrap3'
	)
	admin.add_view(ArticleView(models.Article, db.session))
	admin.add_view(AuthorView(models.Author, db.session))
	admin.add_view(TagView(models.Tag, db.session))
	admin.add_menu_item(
		AdminMenuLink("Profile (Coming Soon)", url="/admin"),
		target_category="Admin"
	)

	# Context Processors
	# Exposes variables needed for custom login page
	@security.context_processor
	def security_context_processor():
		return dict(
			admin_base_template=admin.base_template,
			admin_view=admin.index_view,
			h=admin_helpers,
			get_url=url_for,
		)

    # for creation in CLI
	if data:
		return (db, user_datastore)