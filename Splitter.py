import nltk

'''
Initial classes borrowed from http://fjavieralba.com/basic-sentiment-analysis-with-python.html
'''

class Splitter(object):
	
	def __init__(self):
		self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
		self.tokenizer = nltk.tokenize.TreebankWordTokenizer()
		
	def split(self, text):
		"""
		input format: a paragraph of text
		output format: a list of lists of words
			e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'too']]
		"""
		
		sentences = self.splitter.tokenize(text)
		tokenized_sentences = [self.tokenizer.tokenize(sent) for sent in sentences]
		
		return tokenized_sentences
		