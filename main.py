import webapp2
from backend.home_controller import HomePage
from backend.admin_controller import *

app = webapp2.WSGIApplication([
	('/', HomePage),

	# Admin Section
	('/admin/register', AdminRegisterPage),
	('/admin/login', AdminLoginPage),
	('/admin/logout', AdminLogoutLink),

	('/admin/project', AdminProjectPage),
	('/admin/project/delete', AdminProjectDeletePage),
	('/admin/project/update', AdminProjectUpdatePage),

	('/admin/category', AdminCategoryPage),
	('/admin/category/delete', AdminCategoryDeletePage),
	('/admin/category/update', AdminCategoryUpdatePage),

	('/admin/setting', AdminSettingPage),
	('/admin/setting/update', AdminSettingUpdatePage),
	], debug=True)
