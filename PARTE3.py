'''
CAPITULO 6
'''
'''Clasificación Supervisada
Ejemplo: Identificar el tipo de género de nombre
'''
from nltk.corpus import names
import nltk
import random

def features(word):
    return {'última letra': word[-1]}

print(features('Shrek'))

def features2(name):
    features = {}
    features["Primera letra"] = name[0].lower()
    features["Última letra"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features
 	
print(features2('John'))

def features3(word):
    return {'Última letra': word[-1:],'Dos últimas letras': word[-2:]}

print(features3('John'))

nombres_etiquetados = ([(name, 'masculino') for name in names.words('male.txt')] +
                  [(name, 'femenino') for name in names.words('female.txt')])
random.shuffle(nombres_etiquetados)
#print(nombres_etiquetados)

featuresets = [(features3(nombre), tipo) for (nombre, tipo) in nombres_etiquetados]

train_set, test_set = featuresets[500:], featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print("Nombre Neo es ",classifier.classify(features3('Neo')))
print("Nombre Trinity es ",classifier.classify(features3('Trinity')))

print(nltk.classify.accuracy(classifier, test_set))

classifierDT = nltk.classify.DecisionTreeClassifier.train(train_set)

print("DT Nombre Neo es ",classifierDT.classify(features3('Neo')))
print("DT Nombre Trinity es ",classifierDT.classify(features3('Trinity')))

print(nltk.classify.accuracy(classifierDT, test_set))

algorithm = 'GIS' #nltk.classify.MaxentClassifier.ALGORITHMS[0]
classifierME = nltk.classify.MaxentClassifier.train(train_set, algorithm, trace=0, max_iter=10)

print("ME Nombre Neo es ",classifierME.classify(features3('Neo')))
print("ME Nombre Trinity es ",classifierME.classify(features3('Trinity')))

print(nltk.classify.accuracy(classifierME, test_set))


'''Clasificación Supervisada
Ejemplo: Identificar el tipo de diálogo
'''
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
print(posts[1].get('class'))

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

featuresets = [(dialogue_act_features(post.text), post.get('class'))
                 for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

'''
CAPITULO 7
'''
'''Chunking
'''

sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
             ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

grammar = "NP: {<DT>?<JJ>*<NN>}" 
cp = nltk.RegexpParser(grammar)
result = cp.parse(sentence)
print(result)
result.draw()

from nltk.corpus import conll2000
print(conll2000.chunked_sents('train.txt'))
print(conll2000.chunked_sents('train.txt', chunk_types=['NP']))

from nltk.corpus import conll2000
cp = nltk.RegexpParser("")
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
print(cp.evaluate(test_sents))


sent = nltk.corpus.treebank.tagged_sents()[22]
print(nltk.ne_chunk(sent, binary=True))
print(nltk.ne_chunk(sent)) 

