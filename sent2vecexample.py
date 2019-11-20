import read_file
import write_file
from gensim.models import Word2Vec
from sentence2vec import Sentence2Vec

# fileName = 'Word_Tokenize'
fileName = ['Word_Tokenize', 'corpus_giaothong_newszing'] #.txt
fileDir = ['./TFIDF/', './datasets/']
listRawSentence = read_file.read_line_to_sentenceList(fileDir[1], fileName[1] + '.txt', '\n')
linkModel = './datasets/{0}2vec.model'.format(fileName[1])
# # train
model = Word2Vec(listRawSentence, size=2, window=5, min_count=1)
model.save(linkModel)
# # loadmodel
# sent2vec = Sentence2Vec(linkModel)
# listVect = []
# for rawSent in listRawSentence:
#     listVect.append(sent2vec.get_vector(rawSent).tolist())
# write_file.list_to_txt(listVect, 'datasets', 'Sent2Vect.txt')