import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from anagram import Anagram
from subanagram import SubAnagram
from addword import AddWord
from services import Services


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class MainHandler(webapp2.RequestHandler):


    def get(self):

        self.response.headers["Content-Type"] = "text/html"

        user = Services().get_current_user()
        word_model = Anagram.query()
        anagram_model = None

        if user:
            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("MyUser", Services().get_current_user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = MyUser(id=user.user_id())
                myuser.put()

            anagram_query = Anagram.query(Anagram.user_id == Services().get_current_user_id())
            inputed_word = self.request.get("input_word").lower()


            if len(inputed_word) > 0:

                if self.request.GET.get("search") == "Search Word":

                    anagram_query = anagram_query.filter(Anagram.inputed_words.IN([inputed_word]))

            anagram_model = anagram_query.fetch()

        else:
            url = users.create_login_url(self.request.uri)


        template_values = {
            "url": url,
            "user": user,
            "anagram_model":anagram_model
        }

        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addword', AddWord),
    ('/subanagram', SubAnagram)
], debug=True)

