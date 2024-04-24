import os
import re
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import operator

# create stemmer
# factory = StemmerFactory()
# stemmer = factory.create_stemmer()

# def load_stopWords():
# 	f = file('stopword.txt', 'r');
# 	return f.readlines()

import nltk
from nltk.corpus import stopwords
 
# nltk.download('stopwords')
stopword_list = stopwords.words('english')

# stopword_list = load_stopWords()	


from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
 

 
def stem_p(doc):

    ps = PorterStemmer()
    stemmed_doc = []
    words = word_tokenize(doc)
    for w in words:
        # print(w, " : ", ps.stem(w))
        stemmed_doc.append(w)
    
    return ' '.join(stemmed_doc)

def cleanData(sentence):
	#sentence = re.sub('[^A-Za-z0-9 ]+', '', sentence)
	#sentence filter(None, re.split("[.!?", setence))
	ret = []
	sentence = stem_p(sentence)	
	for word in sentence.split():
		if not word in stopword_list:
			ret.append(word)
	return " ".join(ret)


def getVectorSpace(cleanSet):
	vocab = {}
	for data in cleanSet:
		for word in data.split():
			vocab[data] = 0
	return vocab.keys()
	
def calculateSimilarity(sentence, doc):
	if doc == []:
		return 0
	vocab = {}
	for word in sentence:
		vocab[word] = 0
	
	docInOneSentence = '';
	for t in doc:
		docInOneSentence += (t + ' ')
		for word in t.split():
			vocab[word]=0	
	
	cv = CountVectorizer(vocabulary=vocab.keys())

	docVector = cv.fit_transform([docInOneSentence])
	sentenceVector = cv.fit_transform([sentence])
	return cosine_similarity(docVector, sentenceVector)[0][0]
	
	
def mmr_summarizer(original_doc, percent = 20, lamb = 0.5):
	sentences = []
	clean = []
	originalSentenceOf = {}

	delimiters = [".", ";"]
	# parts = original_doc.split(delimiters)
	parts = re.split(r"[.;!]", original_doc)
	for part in parts:
		part = part.strip()
		cl = cleanData(part)
		#print cl
		sentences.append(part)
		clean.append(cl)
		originalSentenceOf[cl] = part		
	setClean = set(clean)

	scores = {}
	for data in clean:
		temp_doc = setClean - set([data])
		score = calculateSimilarity(data, list(temp_doc))
		scores[data] = score

	n = percent * len(sentences) / 100
	lambda_mmr = lamb
	summarySet = []
	while n > 0:
		mmr = {}
		#kurangkan dengan set summary
		for sentence in scores.keys():
			if not sentence in summarySet:
				mmr[sentence] = lambda_mmr * scores[sentence] - (1-lambda_mmr) * calculateSimilarity(sentence, summarySet)	
		selected = max(mmr.items(), key=operator.itemgetter(1))[0]	
		summarySet.append(selected)
		n -= 1

	summary_sentences = [originalSentenceOf[sentence].lstrip(' ') for sentence in summarySet]
	# print("PERCENT: ", percent)
	# print(f"LAMBDA: {lamb}")
	# print(f"Summary Sentences: {len(summary_sentences)}")
	# print(f"SUMMARY: {summary_sentences}")
	# return summary_sentences
	summary = ' '.join(summary_sentences)
	return summary

def main():
	a = 0
	doc = """As I reflect on my overall journey since being diagnosed with osteoarthritis (OA), it has been six months now. I am pleased that despite some setbacks along the way, there have been significant improvements made toward achieving optimum physical fitness levels and quality living standards through lifestyle changes, stress management techniques, smart workouts at home and adherence to prescribed treatments from medical professionals. These advancements allow me more freedom when performing daily tasks without experiencing debilitating discomfort caused by persistent inflammations associated with aggressive forms like mine; also reducing potential threats posed against bones generally due their exposed vulnerability during such conditions – allowing us get moving forward again while ensuring safety precautions remain intact throughout each day until reaching our desired state where we may finally reach complete relief!
It starts raining inside head - thoughts about what lies ahead? Questions arise regarding whether enough time was dedicated last week for exercise versus office hours worked late into night causing strain across multiple areas rather than just one part muscle groups needed rest after long run earlier same day before dinner preparations began... It appears these days anything goes wrong will become difficult situation unless proper planning takes place weeks far advance notice given whatever happens next comes around; therefore making sure appropriate action plans put together early so they might be executed smoothly whenever required most efficiently possible giving best performance possible under duress sometimes encountered unexpected obstacles which cannot always avoided but if caught off guard then sufferings amplified exponentially beyond reasonable threshold limits forcing otherwise capable individuals fall short their goals altogether leading them deeper down path misery instead joy found hoped attainment levels promised promise fulfilled achieved thus far achieved thus far thanks everyone help keep things balanced here another successful attempt completed today keeping mind active engaged focusing energies productively resulting contented smiles reward enjoyed sharing experiences gained wisdom learned teaching others follow suite create further opportunities continue build upon established foundation laid groundwork previously established during past few years prior attempts accomplished within tight timeline allowed limited resources available narrow window opportunity presented itself requiring swift efficient utilization maximize impactful presence present moment ensuing outcome favorable nature worth celebratory acknowledgement occasions deserving applause accolades recognition achievements unlocked milestones reached set forth initial stages transitioning process becoming something truly extraordinary incredible demonstratives capabilities
"""
	summary = mmr_summarizer(doc, 30, 0.5)

	# print("SUMMARY: ")
	# print(summary)



if __name__ == "__main__":
	main()