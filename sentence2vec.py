import re
import numpy as np
from numpy import dot
from numpy.linalg import norm
from gensim.models import Word2Vec
from underthesea import word_tokenize

class Sentence2Vec:
    def __init__(self, linkModel: str):
        self.load(linkModel)

    def load(self, linkModel: str):
        self.model = Word2Vec.load(linkModel)

    def get_vector(self, sentence) -> np.ndarray:
        # convert to lowercase, ignore all special characters - keep only
        # alpha-numericals and spaces
        # sentence = re.sub(r'[^A-Za-z0-9\s]', r'', str(sentence).lower())
        vectors = [self.model.wv[w] for w in word_tokenize(sentence)
                   if w in self.model.wv]
        v = np.zeros(self.model.vector_size)
        if (len(vectors) > 0):
            v = (np.array([sum(x) for x in zip(*vectors)])) / v.size
        return v

    def similarity(self, x, y) -> float:
        xv = self.get_vector(x)
        yv = self.get_vector(y)
        score = 0
        if xv.size > 0 and yv.size > 0:
            score = dot(xv, yv) / (norm(xv) * norm(yv))
        return score
