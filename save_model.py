from nltk.tokenize import word_tokenize
from scipy.cluster.vq import kmeans,vq
import os
import pickle
from random import shuffle
from multiprocessing import Process
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

#import nltk
#nltk.download('punkt')

def save_model(max_epochs = 50):
    print('Clustering')
    test = dict()
    with os.scandir('./data') as scanner:
        for entry in scanner:
            if entry.name.startswith('.') or not entry.is_file():
                continue
            with open(entry) as stream:
                test[entry.name] = stream.read()


    # tokenize documents
    tagged_data = [TaggedDocument(words=word_tokenize(content.lower()), tags=[file]) for file, content in list(test.items())]
    shuffle(tagged_data)

    #define a Doc2Vec model
    vec_size = 20
    alpha = 0.025

    model = Doc2Vec(vector_size=40, min_count=2, epochs=30, dm=1)
    model.build_vocab(tagged_data)

    #train a Doc2Vec model
    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,total_examples=model.corpus_count,epochs=model.epochs)

        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
    
    #save pickle file
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

save_model(30)