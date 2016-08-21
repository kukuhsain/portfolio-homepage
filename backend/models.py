import hashlib
import random
from string import letters
from google.appengine.ext import ndb

class HashingPassword():
	def make_salt(self, length=5):
		return ''.join(random.choice(letters) for x in xrange(length))

	def make_hashing_password(self, name, password, salt=None):
		if not salt:
			salt = self.make_salt()
			print 'salt: '+salt
		h = hashlib.sha256(str(name)+str(password)+str(salt)).hexdigest()
		return '%s,%s' % (salt, h)

	def validate_password(self, name, password, h):
		salt = h.split(',')[0]
		return h == self.make_hashing_password(name, password, salt)


class Admin(ndb.Model):
	# userid = ndb.IntegerProperty(required=True)
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_user_by_username(cls, username):
		user = cls.query(cls.username==username).get()
		print user
		return user

	@classmethod
	def register(cls, username, password, email=None):
		user = cls.get_user_by_username(username)
		if not user:
			hashed_password = HashingPassword().make_hashing_password(username, password)
			new_admin = cls(username=username, password=hashed_password, email=email)
			new_admin.put()
			return new_admin.key.id()
		else:
			return False

	@classmethod
	def login(cls, username, password):
		user = cls.get_user_by_username(username)
		if user:
			password_validation_result = HashingPassword().validate_password(username, password, user.password)
			if password_validation_result:
				return user.key.id()
			else:
				return False
		else:
			return False

class Category(ndb.Model):
	content = ndb.StringProperty(required=True)
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def add(cls, content):
		parent = ndb.Key('Admin', 'elektromedik umy')
		new_category = cls(parent=parent, content=content)
		new_category.put()

	@classmethod
	def get_all(cls):
		ancestor = ndb.Key('Admin', 'elektromedik umy')
		all_category = cls.query(ancestor=ancestor).order(-cls.created_date).fetch()
		return all_category

	@classmethod
	def get_some(cls, amount):
		ancestor = ndb.Key('Admin', 'elektromedik umy')
		some_category = cls.query(ancestor=ancestor).order(-cls.created_date).fetch(amount)
		return some_category

	@classmethod
	def get_image(cls, key):
		image_key = ndb.Key(urlsafe=key)
		return image_key.get().image

	@classmethod
	def update(cls, id, content):
		parent = ndb.Key('Admin', 'elektromedik umy')
		updated_category = cls.get_by_id(id=int(id), parent=parent)
		updated_category.content = content
		updated_category.put()

	@classmethod
	def delete(cls, id):
		parent = ndb.Key('Admin', 'elektromedik umy')
		cls.get_by_id(id=int(id), parent=parent).key.delete()

class Project(ndb.Model):
	name = ndb.StringProperty(required=True)
	image = ndb.BlobProperty()
	description = ndb.StringProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def add(cls, name, description, image=None):
		parent = ndb.Key('Admin', 'elektromedik umy')
		new_project = cls(parent=parent, name=name, image=image, description=description)
		new_project.put()

	@classmethod
	def get_all(cls):
		ancestor = ndb.Key('Admin', 'elektromedik umy')
		all_project = cls.query(ancestor=ancestor).order(cls.created_date).fetch()
		return all_project

	@classmethod
	def get_image(cls, key):
		image_key = ndb.Key(urlsafe=key)
		return image_key.get().image

	@classmethod
	def update(cls, id, name, image, description):
		parent = ndb.Key('Admin', 'elektromedik umy')
		updated_project = cls.get_by_id(id=int(id), parent=parent)
		updated_project.name = name
		if image:
			updated_project.image = image
		updated_project.description = description
		updated_project.put()

	@classmethod
	def delete(cls, id):
		parent = ndb.Key('Admin', 'elektromedik umy')
		cls.get_by_id(id=int(id), parent=parent).key.delete()

class AdminSetting(ndb.Model):
	photo = ndb.BlobProperty()
	name = ndb.StringProperty()
	description = ndb.StringProperty()
	link_names = ndb.StringProperty(repeated=True)
	link_urls = ndb.StringProperty(repeated=True)

	@classmethod
	def update(cls, photo, name, description, link_names=[], link_urls=[]):
		parent = ndb.Key('Admin', 'elektromedik umy')
		if cls.get():
			admin_setting = cls.get()
			if photo:
				admin_setting.photo = photo
			if :
				admin_setting. =
			admin_setting.name = name
			admin_setting.description = description
			admin_setting.link_names = link_names
			admin_setting.link_urls = link_urls
			admin_setting.put()
		else:
			new_setting_config = cls(parent=parent, photo=photo, name=name, description=description, link_names=link_names, link_urls=link_urls)
			new_setting_config.put()

	@classmethod
	def get(cls):
		ancestor = ndb.Key('Admin', 'elektromedik umy')
		return cls.query(ancestor=ancestor).get()

	@classmethod
	def get_photo(cls):
		return cls.get().photo

class AdminSetting(ndb.Model):
	logo = ndb.BlobProperty()
	cover_image = ndb.BlobProperty()
	title = ndb.StringProperty()
	tagline = ndb.StringProperty()
	link_names = ndb.StringProperty(repeated=True)
	link_urls = ndb.StringProperty(repeated=True)

	@classmethod
	def update(cls, logo, cover_image, title, tagline, link_names=[], link_urls=[]):
		parent = ndb.Key('Admin', 'elektromedik umy')
		if cls.get():
			admin_setting = cls.get()
			if logo:
				admin_setting.logo = logo
			if cover_image:
				admin_setting.cover_image = cover_image
			admin_setting.title = title
			admin_setting.tagline = tagline
			admin_setting.link_names = link_names
			admin_setting.link_urls = link_urls
			admin_setting.put()
		else:
			new_setting_config = cls(parent=parent, logo=logo, cover_image=cover_image, title=title, tagline=tagline, link_names=link_names, link_urls=link_urls)
			new_setting_config.put()

	@classmethod
	def get(cls):
		ancestor = ndb.Key('Admin', 'elektromedik umy')
		return cls.query(ancestor=ancestor).get()

	@classmethod
	def get_logo(cls):
		return cls.get().logo

	@classmethod
	def get_cover_image(cls):
		return cls.get().cover_image
