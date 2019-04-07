import webapp2
import os
import jinja2

from google.appengine.api import users

from anagram import Anagram
from services import Services

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class AddWord(webapp2.RedirectHandler,Services):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"



        template_values = {

        }

        template = JINJA_ENVIRONMENT.get_template("addword.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        if self.request.get("addword") == "Add Word":
            user_word = self.request.get("word").lower()

            if Services().get_current_user() == None or user_word == None or user_word == "" :
                self.redirect("/addword")
                return

            current_user_id = Services().get_current_user_id()
            sorted_key = Services().sorted_key(word =user_word)

            list_word = Anagram.query()
            list_word = list_word.filter(Anagram.anagram_key == sorted_key,Anagram.user_id == current_user_id)
            list_word = list_word.fetch()

            valid_permutation = Services().validpermutations(text=sorted_key)


            if len(valid_permutation) == 0:
                self.redirect("/addword")
                return

            if len(list_word) > 0:
                anagram = list_word[0]

                if user_word in anagram.inputed_words:
                    self.redirect("/addword")
                    return

                inputed_words = anagram.inputed_words
                inputed_words.append(user_word)
                anagram.inputed_words = inputed_words
                anagram.inputed_words_count = anagram.inputed_words_count + 1
                anagram.put()

            else:

                new_anagram = Anagram(anagram_key=sorted_key,
                                   anagram_words = Services().possiblepermutations(text=sorted_key),
                                   inputed_words = [user_word],
                                   inputed_words_count = 1,
                                   word_length = len(user_word),
                                   user_id = current_user_id)
                new_anagram.put()

        self.redirect("/")