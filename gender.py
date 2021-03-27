from pathlib import Path
import json
import codecs
import gensim.models
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import os
from time import time
from kmeans import recluster

# get a vector from a word
def get_vector(word):
    try:
        v = model[word.lower()]
        return v
    except Exception:
        return "I do not know this one, did you mean 'pizza' "

# load text files from the server
def load_files():
    contents = dict()
    with os.scandir('./data') as scanner:
        for entry in scanner:
            if entry.name.startswith('.') or not entry.is_file():
                continue

            with open(entry) as stream:
                contents[entry.name] = stream.read()

    return contents

def delete_file(file_name):
    os.unlink('./data/' + file_name)
    recluster()

# compare two words and get the similarity value
def get_score(w1,w2):
    cs = cosine_similarity(w1.reshape(1, -1),w2.reshape(1, -1))[0][0]
    return cs

# create a json file with whenever the "upload" button is pressed
def upload_text(text):
	if len(text) > 0:
		with open("./data/data_"+str(time())+".txt","w") as file:
			file.write(text)
		recluster()

#you load the model here - depending on this, the results will be different
# if the file is .bin check has to be True, if it's a .txt False
file ="embeddings/reddit.txt"
check = False

model = gensim.models.KeyedVectors.load_word2vec_format(file, binary=check)
female_names = codecs.open("./men-women/women.txt","r","utf-8").read().strip().split("\n")
male_names = codecs.open("./men-women/men.txt","r","utf-8").read().strip().split("\n")

# you just keep the name and lowercase everything
male_names = [x.split()[0].lower() for x in male_names]

# there's a bit of overlap (mark apparently is also a female name), so we keep only female names that are not also male
female_names = [x.split()[0].lower() for x in female_names if x.split()[0].lower() not in male_names]

# you have way more female name then men, so later we will first check the men, then the female


def compute_similar(word, heOrShe = 'she'):
	try:
		mostSimilar = model.most_similar([word, heOrShe ], topn = 20)
		#parole = [(word, float(get_score(get_vector(word.lower()), model[heOrShe]))) for word, _ in mostSimilar if get_score(get_vector(word.lower()), model[heOrShe]) > 0]
		#parole.sort(key=lambda a: a[1], reverse=True)

		return mostSimilar

	except:
		return
		

def compute_bias(text):

	import spacy
	nlp = spacy.load('en_core_web_sm')

	sentence = text

	doc = nlp(sentence)
	final = [ [],[],[],[] ]

	for sent in doc.sents:
	    keep = []
	    #for each word
	    for token in sent:
	        if token.is_alpha:
	            # to have some info  - read documentation: https://spacy.io/usage/linguistic-features
	            if "NN" in token.tag_:
	                keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])
	            if "PRP" in token.tag_:
	                keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])
	            if "NNS" in token.tag_:
	                keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])
	            if "JJ" in token.tag_:
	                keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])

	    # you keep only the subjects - note: someone has to mention the verb "is" twice, otherwise it's hard to get the second name as a a subject
	    subjects = [x for x in keep if "sub" in x[3]]
	    names = [x[0] for x in subjects]

	    for subj in subjects:
	        # we first check if the name is a male
	        check = False
	        if subj[0].lower() in male_names:
	            #print (subj, "is a man!")

	            # if yes, you add this to the info that you have on him
	            # note: i'm adding "he" or "she" because this is what you will use later to compare with the profession
	            subj.append("he")
	            final[1].append(subj[0])

	            check = True

	        elif subj[0].lower() in female_names:
	            #print (subj, "is a woman!")
	            subj.append("she")
	            final[0].append(subj[0])

	            check = True

	        # if the name is not in the list you compare it with the word embeddings of "he" and "she"
	        # this not always work fine - it works for "federico" and "giulia", not for "giacomo" - funny, uh!

	        if check == False:
	        	try:
		            subj_emb = get_vector(subj[0])
		            if get_score(subj_emb,model["he"])>get_score(subj_emb,model["she"]): 
		                final[1].append(subj[0])
		                subj.append("he")

		            else:
		                subj.append("she")
		                final[0].append(subj[0])
		        except:
		        	continue

	    # here you have the profession, namely the names in the sentence that are not subjects
	    professions = [x for x in keep if x not in subjects]
	    profession_names = [x[0] for x in professions]

	    # for each profession, you get a score on how relevant it is for the name
	    results = {x[0]:{} for x in professions}
	    for prof in professions:

	        diff = []

	        for subj in subjects:
	        	try:
		            score = get_score(get_vector(subj[4]),get_vector(prof[0]))
		            results[prof[0]][subj[0]] = score
		            diff.append(score)
		        except:
		        	continue

	    for prof in results.keys():
	        try:

	            if get_score(get_vector(prof),model["she"]) > get_score(get_vector(prof),model["he"]):
	                 final[0].append(prof)
	            else:
	                final[1].append(prof)

	        except:
	            print (e)

	        res = []
	        for subj in subjects:
	        	try:
		            sc = results[prof][subj[0]]
		            res.append(sc)
		        except:
		        	continue

	        try:
	        	fin_res = abs(res[0]-res[1])
	        	#test = (fin_res*1.0)/0.80 # 0.80 for googleNews Embeddings
	        	test = (fin_res*1.0)/0.30

	        	test = test*100
	        	y = (100 - test) /2
	        	x = 100 - y + 1

	        	if max(res[0],res[1]) == res[0]:
	        		if prof in final[0]:
	        			final[2].append([prof,str(int(x) )])
	        			final[3].append([prof,str(int(y) )])
	        		else:
	        			final[2].append([prof,str(int(y) )])
	        			final[3].append([prof,str(int(x) )])

	        	if max(res[0],res[1]) == res[1]:
	        		if prof in final[0]:
	        			final[2].append([prof,str(int(x) )])
	        			final[3].append([prof,str(int(y) )])
	        		else:
	        			final[2].append([prof,str(int(y) )])
	        			final[3].append([prof,str(int(x) )])

	        except:
	        	try:
		        	femalescore =  get_score(get_vector(prof),model["she"])
		        	malescore = get_score(get_vector(prof),model["he"])
		        	new_res = abs(femalescore-malescore)
		        	test = (fin_res*1.0)/0.30
		        	test = test*100
		        	y = (100 - test) /2
		        	x = 100 - y + 1

		        	if max(femalescore,malescore) == femalescore:
		        		if prof in final[0]:
		        			final[2].append([prof,str(int(x) )])
		        			final[3].append([prof,str(int(y) )])


		        	if max(femalescore,malescore) == malescore:
		        		if prof in final[1]:
		        			final[3].append([prof,str(int(x) )])
		        			final[2].append([prof,str(int(y) )])
		        except:
		        	continue

	return(final)
