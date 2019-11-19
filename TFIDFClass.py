from underthesea import sent_tokenize,word_tokenize
import read_file
import write_file
import math
import re
from collections import OrderedDict, defaultdict

# TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / 
# Number of documents with term t in it).

#Còn thời gian viết hàm kiểm tra kết quả.
class TFIDF:
    def __init__(self, rawSents: list, fileInitName: str):
        self.listRawSentence = rawSents
        self.totalSent = len(self.listRawSentence)
        self.listSentToWord = list()
        self.listTF = list()
        # term at doc == word at sentence
        self.dictWordAtSent = dict(list())
        self.dictIDF = dict()
        self.listUniqueWord = list()
        self.listTFIDF = list(list())

        self.initial_step()

    def set_listSentToWord(self):
        for sent in self.listRawSentence:
            tokens = word_tokenize(sent, format='text').split()
            words = []
            for token in tokens:
                if re.match(r'^\w+$', token):
                    words.append(token)
            self.listSentToWord.append(words)
            
    def set_dictWordAtSent(self):
        for iSent in range(len(self.listSentToWord)):
            for word in self.listSentToWord[iSent]:
                if word not in self.dictWordAtSent:
                    self.dictWordAtSent[word] = [iSent]
                elif iSent not in self.dictWordAtSent[word]:
                    self.dictWordAtSent[word].append(iSent)

    def compute_dictTF_of_a_sent(self, currSent: list) -> dict:
        dictTF = {}
        for word in currSent:
            if word not in dictTF:
                dictTF[word] = 1
            else:
                dictTF[word] += 1
        for word in dictTF:
            # dictTF[word] /= len(dictTF)
            dictTF[word] /= len(currSent)
        return dictTF

    def set_listTF(self):
        for sentSplit in self.listSentToWord:
            self.listTF.append(self.compute_dictTF_of_a_sent(sentSplit))

    def compute_IDF_of_a_word(self, word: str):
        # idfValue = 1
        numer = len(self.listSentToWord)
        if word not in self.listUniqueWord:
            denom = 1
        else:
            denom = len(self.dictWordAtSent[word])
            idfValue = math.log(numer / denom)
        return idfValue
        
    def set_dictIDF(self):
        self.dictIDF = dict.fromkeys(self.dictWordAtSent.keys(), 0)
        numOfDocs = len(self.listSentToWord) # document = sentence
        for (word,_) in self.dictIDF.items():
            denom = len(self.dictWordAtSent[word])
            idfVal = math.log(numOfDocs / denom)
            self.dictIDF[word] = idfVal

        # for (word,_) in self.dictIDF.items():
            # self.dictIDF[word] = self.compute_IDF_of_a_word(word)

    def set_listTFIDF(self):
        for sent in self.listSentToWord:
            tfidfSent = []
            for word in sent:
                a = self.listTF[self.listSentToWord.index(sent)][word] 
                b = self.dictIDF[word]
                tfidfSent.append(a*b)
            self.listTFIDF.append(tfidfSent)

    def set_listUniqueWord(self):
        self.listUniqueWord = list(self.dictWordAtSent.keys())

    def write_outfile(self):
        write_file.list_to_txt(self.listSentToWord, 'TFIDF', 'Word_Tokenize.txt')
        write_file.dict_to_txt(self.dictWordAtSent, 'TFIDF', 'Index_of_word.txt')
        write_file.list_to_txt(self.listTF, 'TFIDF', 'TF.txt')
        write_file.dict_to_txt(self.dictIDF, 'TFIDF', 'IDF.txt')
        write_file.list_to_txt(self.listTFIDF, 'TFIDF', 'TFIDFs.txt')

    def initial_step(self):
        self.set_listSentToWord()
        self.set_dictWordAtSent()
        self.set_listUniqueWord()
        self.set_listTF()
        self.set_dictIDF()
        self.set_listTFIDF()

    def get_topK_TFIDF_index(self, k: int):
        topK = dict()
        dictTFIDFSent = dict()
        topTFIDFSent = list()
        indexTopTFIDFSent = list()
        for sentTFIDF in self.listTFIDF:
            maxTFIDF = max(sentTFIDF)
            topTFIDFSent.append(maxTFIDF)
            indexTopTFIDFSent.append(sentTFIDF.index(maxTFIDF))
        print(topTFIDFSent)
        print()
        print(indexTopTFIDFSent)
        ################################################################

    def get_listSentToVect(self):
        return 1

fileName = 'corpus_giaothong_newszing.txt'
# fileName = 'sentences.txt'
# fileName = 'wikiexample.txt'
listRawSentence = read_file.read_line_to_sentenceList('./datasets/', fileName, '\n')
t = TFIDF(listRawSentence, fileName)
# t.get_topK_TFIDF_index(1)
t.write_outfile()



