from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from scipy.cluster.vq import kmeans,vq
import gensim.models
import os
import pickle
from random import shuffle
from multiprocessing import Process

def save_model(max_epochs = 50):
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
    with open('./static/model.pkl', 'wb') as f:
        pickle.dump(model, f)

def load_model(clusters=7):
    #load pickle file
    with open('./static/model.pkl', 'rb') as f:
        trained_model = pickle.load(f)

    return
    centroids, _ = kmeans(trained_model.docvecs, trained_model.docvecs[range(clusters)])
    super_centroid = sum(centroids) / len(centroids)
    sq_distance_from_super_centroid = lambda centroid: sum([(x - x_0) ** 2 for x, x_0 in zip(centroid, super_centroid)])
    centroids = sorted(centroids, key=sq_distance_from_super_centroid)
    # computes cluster Id for document vectors
    doc_ids,_ = vq(trained_model.docvecs, centroids)
    # zips cluster Ids back to document labels
    doc_labels = dict(zip(trained_model.docvecs.doctags.keys(), doc_ids))

    return doc_labels

reclustering = [None]

def recluster():
    if reclustering[0] is not None and reclustering[0].is_alive():
        reclustering[0].terminate()

    reclustering[0] = Process(target=save_model)
    reclustering[0].start()

    return reclustering[0]