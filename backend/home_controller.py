from base_controller import Handlers

class HomePage(Handlers):
	def get(self):
		data = []
		for i in range(5):
			data.append({
				'title': 'Open Source Project',
				'description': 'This is description of the project',
			})

		self.render("homepage.html", data=data)
