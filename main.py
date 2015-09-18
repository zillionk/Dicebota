import webapp2
import cgi
from google.appengine.api import users

MAIN_PAGE_HTML = """\
<html>
	<body>
		<form action='/roll' method='post'>
			<div><textarea name='content' row='3' clos='60'></textarea></div>
			<div><input type='submit' value='roll dice'></div>
		</form>
	</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write('<html><body>')
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('hello,' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))
        self.response.write('</body></html>')
        self.response.write(MAIN_PAGE_HTML)

class RollDice(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/roll', RollDice),
], debug=True)
