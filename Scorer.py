
class Scorer(object):
	
	def __init__(self):
		pass
		
	def value_of(self, sentiment):
		if sentiment == 'positive': return 1
		if sentiment == 'negative': return -1
		return 0
	
	def operator(self, tags, score):
		if 'inc' in tags:
			score *= 2.0
		elif 'dec' in tags:
			score /= 2.0
		elif 'inv' in tags:
			score *= -1.0
		
		return score	
		
	def sentence_score(self, sentence_tokens):
		'''
		input format:
			e.g.: [[('this', 'this', 'DT'), ('is', 'be', 'VB'), ...
		'''
		previous_tags = None
		sentence_score = 0
		
		for (word, lemma, tags) in sentence_tokens:
			token_score = sum([self.value_of(tag) for tag in tags])
			
			if previous_tags is not None:
				token_score = self.operator(previous_tags, token_score)
			
			sentence_score += token_score
		
		return sentence_score
		
	def score(self, sentences):
		return sum([self.sentence_score(sentence) for sentence in sentences])
		