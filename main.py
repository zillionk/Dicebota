import webapp2
import cgi
import urllib
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

def advanture_key(advanture_name='DEFAULT_ADVANTURE_NAME'):
    return ndb.Key('advanture', advanture_name)

class Author(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Message(ndb.Model):
    author = ndb.StructuredProperty(Author)
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
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        sign_query_params = urllib.urlencode({'advanture_name':
                                              advanture_name})
        self.response.write(MAIN_PAGE_HTML %
                            (sign_query_params, cgi.escape(advanture_name),
                             url, url_linktext))
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
        advanture_name = self.request.get('adventure_name',
                                          DEFAULT_ADVANTURE_NAME)
        the_message = Message(parent=advanture_key(advanture_name))

        if users.get_current_user():
            the_message.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        the_message.content = self.request.get('content')
        the_message.put()

        query_params = {'advanture_name': advanture_name}
        self.redirect('/?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/roll', RollDice),
], debug=True)
