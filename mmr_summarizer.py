""" This module contains the functions for the MMR-based (Maximal Marginal Relevance) summarizer,
which is used in generate_parametric_perona_blogs.py
"""
import os
import re
import sys
import operator

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
 

# nltk.download('stopwords')
stopword_list = stopwords.words('english')
 
def stem_p(doc):
	"""
	Returns the stemmed document using the Porter Stemmer. Used in the clean_data() function to stem words.
	"""
	ps = PorterStemmer()
	stemmed_doc = []
	words = word_tokenize(doc)
	for w in words:
        # print(w, " : ", ps.stem(w))
		stemmed_doc.append(ps.stem(w))
    
	return ' '.join(stemmed_doc)

def clean_data(sentence):
	"""
	Stems sentence and removes stop words from it. Used in the mmr_summarizer() function.
	"""
	#sentence = re.sub('[^A-Za-z0-9 ]+', '', sentence)
	#sentence filter(None, re.split("[.!?", setence))
	ret = []
	sentence = stem_p(sentence)	
	for word in sentence.split():
		if not word in stopword_list:
			ret.append(word)
	return " ".join(ret)

	
def calculate_similarity(sentence, doc):
	"""
	Returns the cosine similarity between a sentence and the document it came from
	using the CountVectorizer. Used in mmr_summarizer() to determine sentences to include
	in the summary using the MMR equation.
	"""
	if doc == []:
		return 0
	vocab = {}
	for word in sentence:
		vocab[word] = 0
	
	doc_in_one_sentence = ''
	for t in doc:
		doc_in_one_sentence += (t + ' ')
		for word in t.split():
			vocab[word]=0	
	
	cv = CountVectorizer(vocabulary=vocab.keys())

	doc_vector = cv.fit_transform([doc_in_one_sentence])
	sentence_vector = cv.fit_transform([sentence])
	return cosine_similarity(doc_vector, sentence_vector)[0][0]
	
	
def mmr_summarizer(original_doc, percent = 20, lamb = 0.5):
	"""
 	Generates the MMR (Maximal Marginal Relevance) based summary of the blog post

	Args:
		original_doc: The blog post to be summarized.
		percent (int, optional): The percentage of sentences from the original_doc to retain in the summary. Defaults to 20.
		lamb (float, optional): The lambda value used in the MMR equation. 
  			Higher lambda values mean we care more about similarity with the sentences that have not already been selected
     		than inter-sentence similarity within the summary set. Defaults to 0.5.

	Returns:
		The blog post summary.
	"""
	sentences = []
	clean = []
	original_sentence_of = {}

	delimiters = [".", ";"]
	# parts = original_doc.split(delimiters)
	parts = re.split(r"[.;!]", original_doc)
	for part in parts:
		part = part.strip()
		cl = clean_data(part)
		#print cl
		sentences.append(part)
		clean.append(cl)
		original_sentence_of[cl] = part		
	set_clean = set(clean)

	scores = {}
	for data in clean:
		temp_doc = set_clean - set([data])
		score = calculate_similarity(data, list(temp_doc))
		scores[data] = score

	n = percent * len(sentences) / 100
	lambda_mmr = lamb
	summary_set = []
	while n > 0:
		mmr = {}
		#kurangkan dengan set summary
		for sentence in scores.keys():
			if not sentence in summary_set:
				mmr[sentence] = lambda_mmr * scores[sentence] - (1-lambda_mmr) * calculate_similarity(sentence, summary_set)	
		selected = max(mmr.items(), key=operator.itemgetter(1))[0]	
		summary_set.append(selected)
		n -= 1

	summary_sentences = [original_sentence_of[sentence].lstrip(' ') for sentence in summary_set]
	# print("PERCENT: ", percent)
	# print(f"LAMBDA: {lamb}")
	# print(f"Summary Sentences: {len(summary_sentences)}")
	# print(f"SUMMARY: {summary_sentences}")
	# return summary_sentences
	summary = ' '.join(summary_sentences)
	return summary

def main():
	a = 0
	doc = \
 		"""
 		As I reflect on my overall journey since being diagnosed with osteoarthritis (OA), it has been six months now. I am pleased that despite some setbacks along the way, there have been significant improvements made toward achieving optimum physical fitness levels and quality living standards through lifestyle changes, stress management techniques, smart workouts at home and adherence to prescribed treatments from medical professionals. These advancements allow me more freedom when performing daily tasks without experiencing debilitating discomfort caused by persistent inflammations associated with aggressive forms like mine; also reducing potential threats posed against bones generally due their exposed vulnerability during such conditions – allowing us get moving forward again while ensuring safety precautions remain intact throughout each day until reaching our desired state where we may finally reach complete relief!
		It starts raining inside head - thoughts about what lies ahead? Questions arise regarding whether enough time was dedicated last week for exercise versus office hours worked late into night causing strain across multiple areas rather than just one part muscle groups needed rest after long run earlier same day before dinner preparations began... It appears these days anything goes wrong will become difficult situation unless proper planning takes place weeks far advance notice given whatever happens next comes around; therefore making sure appropriate action plans put together early so they might be executed smoothly whenever required most efficiently possible giving best performance possible under duress sometimes encountered unexpected obstacles which cannot always avoided but if caught off guard then sufferings amplified exponentially beyond reasonable threshold limits forcing otherwise capable individuals fall short their goals altogether leading them deeper down path misery instead joy found hoped attainment levels promised promise fulfilled achieved thus far achieved thus far thanks everyone help keep things balanced here another successful attempt completed today keeping mind active engaged focusing energies productively resulting contented smiles reward enjoyed sharing experiences gained wisdom learned teaching others follow suite create further opportunities continue build upon established foundation laid groundwork previously established during past few years prior attempts accomplished within tight timeline allowed limited resources available narrow window opportunity presented itself requiring swift efficient utilization maximize impactful presence present moment ensuing outcome favorable nature worth celebratory acknowledgement occasions deserving applause accolades recognition achievements unlocked milestones reached set forth initial stages transitioning process becoming something truly extraordinary incredible demonstratives capabilities
		"""
	summary = mmr_summarizer(doc, 30, 0.5)

	# print("SUMMARY: ")
	# print(summary)



if __name__ == "__main__":
	main()