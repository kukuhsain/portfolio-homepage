import webapp2
from backend.home_controller import HomePage

app = webapp2.WSGIApplication([
	('/', HomePage)
	], debug=True)
