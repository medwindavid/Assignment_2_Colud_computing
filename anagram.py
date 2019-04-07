from google.appengine.ext import ndb

class Anagram(ndb.Model):

    anagram_key = ndb.StringProperty()

    anagram_words = ndb.StringProperty(repeated = True)
    inputed_words = ndb.StringProperty(repeated = True)

    inputed_words_count = ndb.IntegerProperty()
    word_length = ndb.IntegerProperty()

    user_id = ndb.StringProperty()

