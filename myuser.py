from google.appengine.ext import ndb
from anagram import Anagram

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    # anagrams = ndb.StructuredProperty(Anagram, repeated=True)
