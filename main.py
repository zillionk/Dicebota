import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('go cross the great wall and see the world.')

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug = True)