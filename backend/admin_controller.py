from base_controller import Handlers, check_for_admin
from models import *
from settings import Credentials
from google.appengine.api import images

def get_admin_sidebar_status():
	return {
		'dosen': '',
		'project': '',
		'category': '',
		'setting': '',
	}

class AdminRegisterPage(Handlers):
	def get(self):
		self.render("admin/admin-register.html")

	def post(self):
		username = self.request.get('admin-username')
		password = self.request.get('admin-password')
		password_again = self.request.get('admin-password-again')
		email = self.request.get('admin-email')
		secret_password = self.request.get('admin-secret-password')

		if username and password and password_again and email and secret_password:
			if password != password_again:
				error = "Password should be same with Password Again"
				self.render("admin/admin-register.html", error=error)
			elif secret_password != Credentials.SECRET_PASSWORD:
				error = "You've just inputed a wrong secret password"
				self.render("admin/admin-register.html", error=error)
			else:
				adminid = Admin.register(username, password, email)
				if adminid:
					success = "Successfully registering a new admin"
					self.render("admin/admin-register.html", success=success)
				else:
					error = "Username is not available"
					self.render("admin/admin-register.html", error=error)
		else:
			error = "You must fill all inputs of the form"
			self.render("admin/admin-register.html", error=error)


class AdminLoginPage(Handlers):
	def get(self):
		userid = self.read_secure_cookie('aid')
		if userid:
			self.redirect('/admin/dosen')
		else:
			self.render("admin/admin-login.html", css="login.css")

	def post(self):
		username = self.request.get('admin-username')
		password = self.request.get('admin-password')

		userid = Admin.login(username, password)
		if userid:
			self.set_secure_cookie('aid', userid)
			self.redirect('/admin/dosen')
		else:
			error = "Login failed, wrong username and/or password"
			self.render("admin/admin-login.html", css="login.css", error=error)

class AdminLogoutLink(Handlers):
	def get(self):
		self.set_secure_cookie('aid', '')
		self.redirect('/')

	def post(self):
		self.set_secure_cookie('aid', '')
		self.redirect('/')

##############################################################################
# Project
class AdminProjectPage(Handlers):
	@check_for_admin
	def get(self):
		css = "admin.css"
		js = "/statics/js/admin-project.js"
		tag = 'project'

		activation = get_admin_sidebar_status()
		activation['project'] = 'active'

		data = Project.get_all()
		self.render("admin/admin-project.html", css=css, js=js, status=activation, tag=tag, data=data)

	@check_for_admin
	def post(self):
		css = "admin.css"
		js = "/statics/js/admin-project.js"
		tag = 'project'

		image = self.request.get('project-image')
		name = self.request.get('project-nama')
		description = self.request.get('project-deskripsi')

		activation = get_admin_sidebar_status()
		activation['project'] = 'active'

		if image:
			image = images.resize(image, 700, 500)
		else:
			image = None

		Project.add(name=name,
			description=description,
			image=image)
		data = Project.get_all()

		self.render("admin/admin-project.html", css=css, js=js, status=activation, tag=tag, data=data)


class AdminProjectDeletePage(Handlers):
	@check_for_admin
	def get(self):
		self.redirect('/admin/project')

	@check_for_admin
	def post(self):
		projectid = self.request.get('project-id')
		Project.delete(int(projectid))
		self.redirect('/admin/project')

class AdminProjectUpdatePage(Handlers):
	@check_for_admin
	def get(self):
		self.redirect('/admin/project')

	@check_for_admin
	def post(self):
		projectid = self.request.get('project-id')
		image = self.request.get('project-image')
		name = self.request.get('project-nama')
		description = self.request.get('project-deskripsi')

		if image:
			image = images.resize(image, 700, 500)
		else:
			image = None

		Project.update(id=projectid,
			name=name,
			description=description,
			image=image)
		self.redirect('/admin/project')

##############################################################################
# Category
class AdminCategoryPage(Handlers):
	@check_for_admin
	def get(self):
		css = "admin.css"
		js = "/statics/js/admin-category.js"
		tag = 'category'

		activation = get_admin_sidebar_status()
		activation['category'] = 'active'

		data = Category.get_all()

		self.render("admin/admin-category.html", css=css, js=js, status=activation, tag=tag, data=data)

	@check_for_admin
	def post(self):
		css = "admin.css"
		js = "/statics/js/admin-category.js"
		tag = 'category'

		content = self.request.get('category-isi')

		activation = get_admin_sidebar_status()
		activation['category'] = 'active'

		Category.add(content=content)
		data = Category.get_all()

		self.render("admin/admin-category.html", css=css, js=js, status=activation, tag=tag, data=data)


class AdminCategoryDeletePage(Handlers):
	@check_for_admin
	def get(self):
		self.redirect('/admin/category')

	@check_for_admin
	def post(self):
		categoryid = self.request.get('category-id')
		Category.delete(int(categoryid))
		self.redirect('/admin/category')

class AdminCategoryUpdatePage(Handlers):
	@check_for_admin
	def get(self):
		self.redirect('/admin/category')

	@check_for_admin
	def post(self):
		categoryid = self.request.get('category-id')
		content = self.request.get('category-isi')

		Category.update(id=categoryid,
			content=content)
		self.redirect('/admin/category')

class AdminSettingPage(Handlers):
	@check_for_admin
	def get(self):
		activation = get_admin_sidebar_status()
		activation['setting'] = 'active'
		data = AdminSetting.get()
		print "Setting admin: (GET)"
		print data
		self.render("admin/admin-setting.html", status=activation, data=data)

	@check_for_admin
	def post(self):
		logo = self.request.get('setting-logo')
		cover_image = self.request.get('setting-cover-image')
		title = self.request.get('setting-judul')
		tagline = self.request.get('setting-tagline')

		post_items = self.request.POST.items()

		link_names = []
		link_urls = []
		for post_item in post_items:
			if 'setting-link-nama' in post_item[0]:
				link_names.append(post_item[1])
			if 'setting-link-url' in post_item[0]:
				link_urls.append(post_item[1])

		print link_names
		print link_urls

		if logo:
			logo = images.resize(logo, 500, 45)
		else:
			logo = None

		if cover_image:
			cover_image = images.resize(cover_image, 700, 500)
		else:
			cover_image = None

		AdminSetting.update(logo=logo,
			cover_image=cover_image,
			title=title,
			tagline=tagline,
			link_names=link_names,
			link_urls=link_urls)

		activation = get_admin_sidebar_status()
		activation['setting'] = 'active'

		data = AdminSetting.get()

		print "Setting admin: (POST)"
		print data

		self.render("admin/admin-setting.html", status=activation, data=data)

class AdminSettingUpdatePage(Handlers):
	@check_for_admin
	def get(self):
		js = "/statics/js/admin-setting.js"

		activation = get_admin_sidebar_status()
		activation['setting'] = 'active'

		data = AdminSetting.get()

		self.render("admin/admin-setting-update.html", js=js, status=activation, data=data)
