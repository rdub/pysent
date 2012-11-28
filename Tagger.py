import yaml
import nltk

class Tagger(object):
	
	def __init__(self):
		pass
	
	def tag(self, sentences):
		"""
		input format: list of lists of words
			e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'too']]
		output format: depends on subclass
		"""
		raise Exception('Please override this method')
		
class POSTagger(Tagger):
	
	def __init__(self):
		pass
		
	def tag(self, sentences):
		"""
		input format: list of lists of words
			e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'too']]
		output format: list of lists of tagged tokens, each tagged token has a form, and a tag:
			e.g.: [[('this', 'DT'), ('is', 'VB'), ...
		"""
		pos = [nltk.pos_tag(sentence) for sentence in sentences]
		return pos

class DictionaryTagger(Tagger):
	'''
	Does POS tagging transparently
	'''
	
	def __init__(self, dict_paths):
		files = [open(path, 'r') for path in dict_paths]
		dictionaries = [yaml.load(dict_file) for dict_file in files]
		map(lambda x: x.close(), files)
		
		self.dictionary = {}
		self.max_key_size = 0
		
		for curr_dict in dictionaries:
			for key in curr_dict:
				if not key in self.dictionary:
					self.dictionary[key] = list()
					self.max_key_size = max(self.max_key_size, len(key))
					
				self.dictionary[key].extend(curr_dict[key])
		self.wn = nltk.stem.wordnet.WordNetLemmatizer()
				
	def lemma(self, word, postag):
		if 'VB' in postag:
			return self.wn.lemmatize(word, 'v')
		return self.wn.lemmatize(word)
	
	def tag(self, sentences):
		'''
		input format: list of lists of tuples (word, postag)
			e.g.: [[('this', 'DT'), ('is', 'VB'), ...
		output format: list of lists of tagged tokens, each tagged token has a form, a lemma, and a tag:
			e.g.: [[('this', 'this', 'DT'), ('is', 'be', 'VB'), ...
		'''
		# Support [[('this', 'DT'), ('is', 'VB') ...]] and [['this', 'is' ...], ['this', 'too']]
		if not isinstance(sentences, list):
			raise Exception('Invalid data type')
		
		if not isinstance(sentences[0], list):
			raise Exception('Invalid data type')
		
		if isinstance(sentences[0][0], str):
			# Second form, call POS Tagger first
			p = POSTagger()
			sentences = p.tag(sentences)
		
		# Already POS tagged, adapt format for the next step
		sentences = [[(word, self.lemma(word, postag), [postag]) for (word, postag) in sentence] for sentence in sentences]
		
		return [self.tag_sentence(sentence) for sentence in sentences]
	
	def tag_sentence(self, sentence, tag_with_lemmas=False):
		"""
		the result is only one tagging of all the possible ones.
		The resulting tagging is determined by these two priority rules:
			- longest matches have higher priority
			- search is made from left to right
		"""
		tagged_sentence = []
		N = len(sentence)
		
		if self.max_key_size == 0:
			self.max_key_size = N
		
		i = 0
		while(i < N):
			j = min(i + self.max_key_size, N)
			tagged = False
			
			while(j > i):
				expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
				expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
				if tag_with_lemmas:
					literal = expression_lemma
				else:
					literal = expression_form
				
				if literal in self.dictionary:
					is_single_token = j - i == 1
					original_pos = i
					i = j
					taggings = [tag for tag in self.dictionary[literal]]
					tagged_expression = (expression_form, expression_lemma, taggings)
					
					if is_single_token:
						original_token_tagging = sentence[original_pos][2]
						tagged_expression[2].extend(original_token_tagging)
					
					tagged_sentence.append(tagged_expression)
					tagged = True
				else:
					j = j - 1
			if not tagged:
				tagged_sentence.append(sentence[i])
				i += 1
		return tagged_sentence
		
				
					
					