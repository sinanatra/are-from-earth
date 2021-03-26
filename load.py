from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy.cluster.vq import kmeans,vq
import pickle
from random import shuffle

def load_model(clusters=7):
    #load pickle file
    with open('model.pkl', 'rb') as f:
        trained_model = pickle.load(f)

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

load_model()