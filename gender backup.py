def get_vector(word):
    try:
        v = model[word.lower()]
        return v
    except Exception:
        return "I do not know this one, did you mean 'pizza' "


from sklearn.metrics.pairwise import cosine_similarity

# compare two words and get the similarity value
def get_score(w1,w2):

    cs = cosine_similarity(w1.reshape(1, -1),w2.reshape(1, -1))[0][0]

    return cs

#you load the model here - depending on this, the results will be different
# if the file is .bin check has to be True, if it's a .txt False

#file = "/Users/sinanatra/Google Drive/Programming/embeddings/GoogleNews-vectors-negative300.bin"
file ="/Users/sinanatra/Documents/GitHub/gender-bias-embedding/models/reddit.txt"

check = False

import gensim.models
model =gensim.models.KeyedVectors.load_word2vec_format(file,
                                                       binary=check)

import codecs
female_names = codecs.open("./men-women/women.txt","r","utf-8").read().strip().split("\n")
male_names = codecs.open("./men-women/men.txt","r","utf-8").read().strip().split("\n")

# you just keep the name and lowercase everything
male_names = [x.split()[0].lower() for x in male_names]

# there's a bit of overlap (mark apparently is also a female name), so we keep only female names that are not also male
female_names = [x.split()[0].lower() for x in female_names if x.split()[0].lower() not in male_names]

# you have way more female name then men, so later we will first check the men, then the female
print (len(female_names),len(male_names))


def compute_bias(text):

	# you load here names of men and women (english names for the moment)

	import spacy
	nlp = spacy.load('en')

	sentence = text
	print(sentence)
	doc = nlp(sentence)
	# you loop over the sentences if someone writes more than one (i hope not)
	for sent in doc.sents:

		keep = []

		#for each word
		for token in sent:
		    #if word is not a number
		    if token.is_alpha:
		        # you keep only the nouns (so hopefully only subjects and professions)
			    if "NN" in token.tag_:
				# you have some info  - read documentation: https://spacy.io/usage/linguistic-features
				    keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])

			    if "PRP" in token.tag_:

				    keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])

			    if "NNS" in token.tag_:

				    keep.append([token.orth_, token.tag_, token.head.lemma_, token.dep_])

		 # you keep only the subjects (token.dep_) - note: someone has to mention the verb "is" twice, otherwise it's hard to get the second name as a a subject - (to fix later)
		subjects = [x for x in keep if "sub" in x[3]]

		for subj in subjects:

		# we first check if the name is a male
			check = False
			if subj[0].lower() in male_names:
			    #print (subj, "is a man!")

			    # if yes, you add this to the info that you have on him
			    # note: i'm adding "he" or "she" because this is what you will use later to compare with the profession
			    subj.append("he")
			    check = True

			elif subj[0].lower() in female_names:
			    #print (subj, "is a woman!")
			    subj.append("she")

			    check = True

		# if the name is not in the list you compare it with the word embeddings of "he" and "she"
		# this not always work fine - it works for "federico" and "giulia", not for "giacomo" - funny, uh! - (it depends by the embedding file)

			if check == False:

			    try:
			        subj_emb = get_vector(subj[0])
			        if get_score(subj_emb,model["he"])>get_score(subj_emb,model["she"]):
			            #print (subj, "is a man!","embed")
			            subj.append("he")
			        else:
			            #print (subj, "is a woman!","embed")
			            subj.append("she")
			    except Exception:
			        print("Uops! i don't recognize the name "+ subj[0] )


		# here you have the profession, namely the names in the sentence that are not subjects
		professions = [x for x in keep if x not in subjects]

		# for each profession, you get a score on how relevant it is for the name
		for prof in professions:
			try:
				print("entra qua")
				for subj in subjects:
					score = get_score(get_vector(subj[4]),get_vector(prof[0]))
					subj.append([prof[0],float(score)])

			except Exception as e:
			    print (e)
		# here you have the score
		for subj in subjects:
			print (subj)




		return subjects
