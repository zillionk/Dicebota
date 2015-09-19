import webapp2
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb


MAIN_PAGE_HTML = """\
    <form action='/roll?%s' method='post'>
   		<div><textarea name='content' row='3' clos='60'></textarea></div>
    	<div><input type='submit' value='roll dice'></div>
    </form>
    <form>Dice Result:
    	<input value='%s' name="diceResult">
    	<input type="submit" value='switch'>
    </form>
    <a href='%s'>%s</a>
"""
DEFAULT_ADVANTURE_NAME = 'new_advanture'

def advanture_key(adventure_name='DEFAULT_ADVANTURE_NAME'):
    return ndb.Key('advanture', adventure_name)

class Author(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Message(ndb.Model):
    Author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write('<html><body>')
        advanture_name = self.request.get('advanture_name', DEFAULT_ADVANTURE_NAME)
        message_query = Message.query(
        	ancestor = advanture_key(advanture_name)).order(-Message.date)
        messages = message_query.fetch(10)
        for message in messages:
        	if message.author:
        		author = message.author.email
        		self.response.write('<b>%s</b> asked:' % author)
        	else:
        		self.response.write('Anonymous Person wrote:')
        	self.response.write('<blockquote>%s</blockquote>' % cgi.escape(message.content))



        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('hello,' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('</body></html>')
# """
# {
#     chooseInside: True
#     chooseNum: 3
#     diceNum: 4
#     face:6
#     adjust:4
#     comment: test
# }
# """
class RollDice(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/roll', RollDice),
], debug=True)
