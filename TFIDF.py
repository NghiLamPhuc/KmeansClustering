from underthesea import word_tokenize
import read_file
import write_file

def compute_tf(wordDict, bow: list):
    tfDict = {}
    bowCount = len(bow)
    for (word, count) in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def compute_idf(docList):
    import math
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = 1 + math.log10(N / float(val)) # smooth with add 1
        
    return idfDict

def compute_tf_idf(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf

def get_vector_sentence(bow: list, tfidf: dict) -> list:
    vector = []
    for w in bow:
        for (word, prob) in tfidf.items():
            if w == word:
                vector.append(prob)
    return vector

listRawSentence = read_file.read_line_to_sentenceList('./datasets/', 'motVaiCau.txt', '\n')
sentenceCount = len(listRawSentence)
listSentenceToWord = []
for sent in listRawSentence:
    listSentenceToWord.append(word_tokenize(sent, format='text'))
listBow = list()
for sentWord in listSentenceToWord:
    listBow.append(sentWord.split())

wordSet = list({x for _list in listBow for x in _list})

listWordDict = list()
for _ in range(sentenceCount):
    listWordDict.append(dict.fromkeys(wordSet, 0))

for index in range(sentenceCount):
    for sentWord in listSentenceToWord:
        for word in sentWord.split():
            listWordDict[index][word] += 1
listTF = []
for index in range(sentenceCount):
    listTF.append(compute_tf(listWordDict[index], listSentenceToWord[index].split()))

idfs = compute_idf(listWordDict)

listTFIDF = []
for index in range(sentenceCount):
    listTFIDF.append(compute_tf_idf(listTF[index], idfs))

listVector = []
for tfidfDict in listTFIDF:
    vector = []
    for (word, tfidf) in tfidfDict.items():
        vector.append(tfidf)
    listVector.append(vector)

write_file.list_to_txt_with_last_comma(listVector, './datasets/', 'vectorize.txt', ' ')