import webapp2
import jinja2
import os


from anagram import Anagram
from services import Services


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class SubAnagram(webapp2.RequestHandler):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"

        inputed_word = self.request.GET.get("input_word")

        sorted_key = Services().sorted_key(word=inputed_word)
        list_sorted_keys = []

        anagram_query = Anagram.query(Anagram.user_id == Services().get_current_user_id())

        possible_combination_key = Services().possibleAllCountPermutations(text=sorted_key)
        anagram_models = []

        for word in possible_combination_key:

            query = anagram_query.filter(Anagram.anagram_key == word).fetch(projection=[Anagram.inputed_words])
            if len(query) > 0:

                for anagram in query:
                    anagram_models.extend(anagram.inputed_words)

        dictionary_words = {}
        for word in anagram_models:

            if len(word) in dictionary_words:
                dict_words = dictionary_words[len(word)]
                dict_words.append(word)
                dictionary_words[len(word)] = dict_words
            else:
                dictionary_words[len(word)] = [word]

        template_values = {
            "inputword":inputed_word,
            "dictionary_words": dictionary_words
        }

        template = JINJA_ENVIRONMENT.get_template("subanagram.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        if self.request.get("cancel"):
            self.redirect("/")
