import webapp2
import os
import jinja2
import hmac
from functools import wraps
from settings import Credentials


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class HashingCookie():
	def hash_str(self, s):
		return hmac.new(Credentials.SECRET_COOKIE, s).hexdigest()

	def make_secure_value(self, s):
		return "%s|%s" % (s, self.hash_str(s))

	def check_secure_value(self, s):
		value = s.split('|')[0]
		if s == self.make_secure_value(value):
			return value
		else:
			return False

class Handlers(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, value):
		if value:
			cookie_value = HashingCookie().make_secure_value(str(value))
		else:
			cookie_value = ''
		self.response.headers.add_header('Set-Cookie', '%s=%s' % (name, cookie_value))

	def read_secure_cookie(self, name):
		cookie_value = self.request.cookies.get(name)
		if cookie_value:
			return HashingCookie().check_secure_value(cookie_value)
		else:
			return False


def check_for_admin(f):
	@wraps(f)
	def wrapper(self):
		adminid = self.read_secure_cookie('aid')
		if adminid:
			f(self)
		else:
			self.redirect('/')
	return wrapper


app = webapp2.WSGIApplication([
	('/', HomePage)
	], debug=True)
