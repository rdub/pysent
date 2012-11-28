#!/usr/bin/env python

import Splitter
import Tagger
import Scorer
import Importer

import yaml
from pprint import pprint

if __name__ == "__main__":
	rss = Importer.RSSImporter('https://news.google.com/news/feeds?q=apple&output=rss')
	input_text = rss.parse()
	
	s = Splitter.Splitter()
	tagger = Tagger.DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml', 
										'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
	scorer = Scorer.Scorer()
	total = 0
	for summary in input_text:
						
		split = s.split(summary)
	
		tagged = tagger.tag(split)
	
		score = scorer.score(tagged)
		print "%s -> %d" % (summary, score)
		total += score
	
	print "Total: %d" % total