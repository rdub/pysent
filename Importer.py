
class Importer(object):
	def __init__(self):
		pass

import feedparser
from pprint import pprint

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

import htmlentitydefs
import re

def convertentity(m):
	if m.group(1)=='#':
		try:
			return unichr(int(m.group(2)))
		except ValueError:
			return '&#%s;' % m.group(2)
		try:
			return htmlentitydefs.entitydefs[m.group(2)]
		except KeyError:
			return '&%s;' % m.group(2)

def converthtml(s):
	return re.sub(r'&(#?)(.+?);',convertentity,s)

import unicodedata

class RSSImporter(Importer):
	def __init__(self, url):
		self.url = url
		self.feed = None
		
	def load(self):
		self.feed = feedparser.parse(self.url)
		
	def strip_tags(self, post):
		stripper = MLStripper()
		stripper.feed(post)
		return converthtml(stripper.get_data())
	
	def parse(self):
		if(self.feed == None):
			self.load()
			
		sentences = []
		for item in self.feed['items']:
			summary = self.strip_tags(item['summary_detail']['value'])
			sentences.append(unicodedata.normalize('NFKD', summary).encode('ascii','ignore'))
		
		#pprint(sentences)
		return sentences
