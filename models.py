import datetime

from extensions import db
from flask_security import UserMixin, RoleMixin

from wtforms import TextAreaField
from wtforms.widgets import TextArea, Select
from wtforms.utils import unset_value 

from flask_admin.form import Select2TagsField

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy_utils.types.choice import ChoiceType


STATUS = [(u'0', u"Draft"), (u'1', u"Published")]


# Relationship Tables
roles_users = db.Table('roles_users',
	Column('user_id', Integer, ForeignKey('user.id')),
	Column('role_id', Integer, ForeignKey('role.id'))
)

articles_tags = db.Table('articles_tags',
	Column('article_id', Integer, ForeignKey('article.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)

# Security/Admin Models
class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(128))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.String(80), unique=True, nullable=False)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	password = db.Column(db.String(80), nullable=False)
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Role',
		secondary=roles_users,
		backref=db.backref('users', lazy='dynamic')
	)

# Models for articles
class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(80), unique=True)
	bio = db.Column(db.String(500))
	image = db.Column(db.String(80))
	articles = db.relationship("Article", backref="author", lazy=True)

	def __repr__(self):
		return "%s %s" % (self.first_name, self.last_name)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	permalink = db.Column(db.String(255))
	date_published = db.Column(db.DateTime())
	last_edited = db.Column(db.DateTime())
	status = db.Column(ChoiceType(STATUS))
	body = db.Column(db.String(10000))
	tag = db.relationship('Tag', secondary=articles_tags,
		backref=db.backref('articles', lazy='dynamic')
	)
	author_id = db.Column(Integer, db.ForeignKey('author.id'), nullable=False)

	def __repr__(self):
		return "Article: %r" % self.title

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)

	def __repr__(self):
		return self.name


# Fields for views
class SKNTextAreaWidget(TextArea):
	def __call__(self, field, **kwargs):
		kwargs.setdefault('class_', 'ckeditor')
		return super(SKNTextAreaWidget, self).__call__(field, **kwargs)

class SKNTextAreaField(TextAreaField):
	widget = SKNTextAreaWidget()


class SKNAdvancedTagWidget(Select):
	"""
	Select2 <https://github.com/select2/select2>
	You must include select2.js, form-x.x.x.js and select2 stylesheet

	Creates the html to be rendered on the template
	"""
	def __call__(self, field, **kwargs):
		kwargs.setdefault('data-tags', 1)
		allow_blank = getattr(field, 'allow_blank', False)
		if allow_blank and not self.multiple:
			kwargs['data-allow-blank'] = u'1'
		return super(SKNAdvancedTagWidget, self).__call__(field, **kwargs)

class SKNAdvancedTagField(Select2TagsField):
	"""
	Custom tag field. Supports tags that do not exist yet.
	Sets the behaviour of the Field
	"""
	widget = SKNAdvancedTagWidget(multiple=True)

	def pre_validate(self, form):
		pass

	def process_formdata(self, valuelist):
		# valuelist is the list of tags that the user input.
		if valuelist:
			self.data = []
			for tagname in valuelist:
				rv = Tag.query.filter_by(name=tagname).first()
				if rv:
					self.data.append(rv)
				else:
					self.data.append(Tag(name=tagname))

		else:
			self.data=[]

	def iter_choices(self):
		""" 
		Must yield (value, label, selected)
		"""

		self.blank_text = ""
		tags = [str(tag.name) for tag in Tag.query.all()]
		if self.object_data:
			model_tags = [str(tag.name) for tag in self.object_data]
		else:
			model_tags = []

		self.choices = [[tag, tag] for tag in tags]

		# shows options
		for value, label, in self.choices:
			yield (value, label, value in model_tags)