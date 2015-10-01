import webapp2
import cgi
import urllib
import logging
import jinja2
import json
import re

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from variables import *

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
        # logging.debug('I come from MainPage, current adv_name is: '+ advanture_name)
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
#     chooseAmong: True
#     chooseNum: 3
#     diceNum: 4
#     face:6
#     adjust:4
#     comment: test
# }
# """
class RollDiceWrapper(webapp2.RequestHandler):
    def post(self):
        advanture_name = self.request.get('advanture_name',
                                          DEFAULT_ADVANTURE_NAME)
        the_message = Message(parent=advanture_key(advanture_name))

        if users.get_current_user():
            the_message.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        # pass data to dice roller, and get return value
        meta_data = SplitString(self.request.get('content'))
        data = urllib.urlencode({'content':meta_data})
        result = urlfetch.fetch(API_URL+'dice?%s' % data)
        the_message.content = json.loads(result.content)['content']
        the_message.put()
        query_params = {'advanture_name': advanture_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class SwitchAdvanture(webapp2.RequestHandler):
	def post(self):
		advanture_name = self.request.get('advanture_name',
                                          DEFAULT_ADVANTURE_NAME)

# get the order string, and get dice data from it.        
def SplitString(the_order):
    matches = re.search(RE_FETCH_DICE_ROLL, the_order)
    if matches is None:
        return "Error: Wrong command. please used fomula like '1d6+3'"
    else:   
        return matches.group(0)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/roll', RollDiceWrapper),
    ('/switch', SwitchAdvanture),
], debug=True)
