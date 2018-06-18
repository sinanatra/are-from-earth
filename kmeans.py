from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from scipy.cluster.vq import kmeans,vq
import gensim.models
import os
import pickle

def save_model():
    test = dict()
    with os.scandir('./data') as scanner:
        for entry in scanner:
            if entry.name.startswith('.') or not entry.is_file():
                continue
            with open(entry) as stream:
                test[entry.name] = stream.read()

    #print("contents" , contents,"test" , test.keys())


    # tokenize documents
    tagged_data = [TaggedDocument(words=word_tokenize(content.lower()), tags=[file]) for file, content in list(test.items())]

    #define a Doc2Vec model
    max_epochs = 500
    vec_size = 20
    alpha = 0.025

    model = Doc2Vec(size=vec_size,
                    alpha=alpha,
                    min_alpha=0.025,
                    min_count=3,
                    dm =1)
    model.build_vocab(tagged_data)

    #train a Doc2Vec model
    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    #save pickle file
    with open('model.pkl', 'wb') as f:
        print("pippo")
        pickle.dump(model, f)

def load_model():
    #load pickle file
    with open('model.pkl', 'rb') as f:
        trained_model = pickle.load(f)

    #define the number of clusters
    clusters = 5
    centroids, _ = kmeans(trained_model.docvecs, clusters)
    # computes cluster Id for document vectors
    doc_ids,_ = vq(trained_model.docvecs, centroids)
    # zips cluster Ids back to document labels
    doc_labels = dict(zip(trained_model.docvecs.doctags.keys(), doc_ids))

    return doc_labels
