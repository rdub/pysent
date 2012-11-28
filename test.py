#!/usr/bin/env python

import Splitter
import Tagger
import Scorer
import Importer

import yaml
from pprint import pprint

if __name__ == "__main__":
	text = """What can I say about this place. The staff of the restaurant is 
	nice and the eggplant is not bad. Apart from that, very uninspired food, 
	lack of atmosphere and too expensive. I am a staunch vegetarian and was 
	sorely dissapointed with the veggie options on the menu. Will be the last 
	time I visit, I recommend others to avoid."""

	rss = Importer.RSSImporter('https://news.google.com/news/feeds?q=apple&output=rss')
	input_text = rss.parse()
	
	s = Splitter.Splitter()
	tagger = Tagger.DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml', 
										'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
	scorer = Scorer.Scorer()
	total = 0
	for summary in input_text:
						
		split = s.split(summary)
		#pprint(split)
	
		tagged = tagger.tag(split)
		#pprint(tagged)
	
		score = scorer.score(tagged)
		print "%s -> %d" % (summary, score)
		total += score
	
	print "Total: %d" % total