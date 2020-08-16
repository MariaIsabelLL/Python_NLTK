#from nltk.book import *
from nltk.corpus import movie_reviews 
from nltk import FreqDist
from random import shuffle 
from nltk.corpus import stopwords
import string
from nltk import NaiveBayesClassifier
from nltk import classify 
from nltk.tokenize import word_tokenize
from nltk import ngrams

def Estadisticas():
    
    print ('total',len(movie_reviews.fileids())) 
    print ('categorias',movie_reviews.categories()) 
    print ('total positivos',len(movie_reviews.fileids('pos')))
    print ('total negativos',len(movie_reviews.fileids('neg'))) 
     
    all_words = [word.lower() for word in movie_reviews.words()]
    all_words_frequency = FreqDist(all_words)
    print ('10 palabras más frecuentes',all_words_frequency.most_common(10))
    print ('cantidad de veces que se repite la palabra happy',all_words_frequency['happy'])

'''
Top-N words feature
'''

def Datos():
    documents = []     
    for category in movie_reviews.categories():
        for fileid in movie_reviews.fileids(category):
            documents.append((movie_reviews.words(fileid), category))
    shuffle(documents)
    
    stopwords_english = stopwords.words('english')
    all_words = [word.lower() for word in movie_reviews.words()]
    all_words_clean = []
    for word in all_words:
        if word not in stopwords_english and word not in string.punctuation:
            all_words_clean.append(word)
    
    all_words_frequency = FreqDist(all_words_clean)
    print (all_words_frequency.most_common(10))    
    most_common_words = all_words_frequency.most_common(2000)
    print (most_common_words[:10])
    word_features = [item[0] for item in most_common_words]
    
    return documents, word_features

def document_features(document,word_features):      
    document_words = set(document)    
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
    
def clasificador(documents,word_features):    
    feature_set = [(document_features(doc,word_features), category) 
                    for (doc, category) in documents]
    size = int(len(feature_set) * 0.2) 
    test_set = feature_set[:size]
    train_set = feature_set[size:]     
    print (len(train_set))
    print (len(test_set)) 
    
    classifier = NaiveBayesClassifier.train(train_set)
    accuracy = classify.accuracy(classifier, test_set)
    print (accuracy) 
    return classifier
    
def prueba(custom_review,classifier,word_features):  
    custom_review_tokens = word_tokenize(custom_review)
    custom_review_set = document_features(custom_review_tokens,word_features)
    print (custom_review) 
    print ('positivo o negativo?',classifier.classify(custom_review_set)) 
    prob_result = classifier.prob_classify(custom_review_set)
    print ('probabilidad para negativo',prob_result.prob("neg")) 
    print ('probabilidad para positivo',prob_result.prob("pos")) 
    
Estadisticas()
(documents,word_features) = Datos()
classifier = clasificador(documents,word_features)
texto = "I hated the film. It was a disaster. Poor direction, bad acting."
prueba(texto,classifier,word_features)
texto = "It was a wonderful and amazing movie. I loved it. Best direction, good acting."
prueba(texto,classifier,word_features)
print (classifier.show_most_informative_features(10))

'''
Bag of Words Feature
'''

def bag_of_words(words):
    words_clean = []
    stopwords_english = stopwords.words('english')
    
    for word in words:
        word = word.lower()
        if word not in stopwords_english and word not in string.punctuation:
            words_clean.append(word)
    
    words_dictionary = dict([word, True] for word in words_clean)
    
    return words_dictionary

def DatosBOW():
    pos_reviews = []
    for fileid in movie_reviews.fileids('pos'):
        words = movie_reviews.words(fileid)
        pos_reviews.append(words)
     
    neg_reviews = []
    for fileid in movie_reviews.fileids('neg'):
        words = movie_reviews.words(fileid)
        neg_reviews.append(words)
        
    pos_reviews_set = []
    for words in pos_reviews:
        pos_reviews_set.append((bag_of_words(words), 'pos'))
     
    neg_reviews_set = []
    for words in neg_reviews:
        neg_reviews_set.append((bag_of_words(words), 'neg'))
        
    return pos_reviews_set,neg_reviews_set

def clasificadorBOW(pos_reviews_set,neg_reviews_set):     
    size = int(len(pos_reviews_set) * 0.1)     
    test_set = pos_reviews_set[:size] + neg_reviews_set[:size]
    train_set = pos_reviews_set[size:] + neg_reviews_set[size:]
    print(len(test_set),  len(train_set))
    classifier = NaiveBayesClassifier.train(train_set) 
    accuracy = classify.accuracy(classifier, test_set)
    print(accuracy)  
    print (classifier.show_most_informative_features(10))
    return classifier

def pruebaBOW(custom_review,classifier):  
    custom_review_tokens = word_tokenize(custom_review)
    custom_review_set = bag_of_words(custom_review_tokens)
    print (custom_review) 
    print ('positivo o negativo?',classifier.classify(custom_review_set)) 
    prob_result = classifier.prob_classify(custom_review_set)
    print ('probabilidad para negativo',prob_result.prob("neg")) 
    print ('probabilidad para positivo',prob_result.prob("pos")) 
    
(pos_reviews_set,neg_reviews_set) = DatosBOW()
clasifierBOW = clasificadorBOW(pos_reviews_set,neg_reviews_set)
texto = "I hated the film. It was a disaster. Poor direction, bad acting."
pruebaBOW(texto,clasifierBOW)
texto = "It was a wonderful and amazing movie. I loved it. Best direction, good acting."
pruebaBOW(texto,clasifierBOW)

'''
Bi-gram Features
'''
def clean_words(words, stopwords_english):
    words_clean = []
    for word in words:
        word = word.lower()
        if word not in stopwords_english and word not in string.punctuation:
            words_clean.append(word)    
    return words_clean 
 
def bag_of_words2(words):    
    words_dictionary = dict([word, True] for word in words)    
    return words_dictionary
 
def bag_of_ngrams(words, n=2):
    words_ng = []
    for item in iter(ngrams(words, n)):
        words_ng.append(item)
    words_dictionary = dict([word, True] for word in words_ng)    
    return words_dictionary

def bag_of_all_words(words, n=2):
    important_words = ['above', 'below', 'off', 'over', 'under', 'more', 'most', 'such', 'no', 'nor', 'not', 'only', 'so', 'than', 'too', 'very', 'just', 'but']
    stopwords_english = stopwords.words('english')
    stopwords_english_for_bigrams = set(stopwords_english) - set(important_words)
    
    words_clean = clean_words(words, stopwords_english)
    words_clean_for_bigrams = clean_words(words, stopwords_english_for_bigrams)
 
    unigram_features = bag_of_words2(words_clean)
    bigram_features = bag_of_ngrams(words_clean_for_bigrams)
 
    all_features = unigram_features.copy()
    all_features.update(bigram_features)
 
    return all_features
    
def DatosNGRAM():
    pos_reviews = []
    for fileid in movie_reviews.fileids('pos'):
        words = movie_reviews.words(fileid)
        pos_reviews.append(words)
     
    neg_reviews = []
    for fileid in movie_reviews.fileids('neg'):
        words = movie_reviews.words(fileid)
        neg_reviews.append(words)
        
    pos_reviews_set = []
    for words in pos_reviews:
        pos_reviews_set.append((bag_of_all_words(words), 'pos'))
     
    neg_reviews_set = []
    for words in neg_reviews:
        neg_reviews_set.append((bag_of_all_words(words), 'neg'))
        
    return pos_reviews_set,neg_reviews_set

def clasificadorNGRAM(pos_reviews_set,neg_reviews_set):     
    shuffle(pos_reviews_set)
    shuffle(neg_reviews_set)
    size = int(len(pos_reviews_set) * 0.1)     
    test_set = pos_reviews_set[:size] + neg_reviews_set[:size]
    train_set = pos_reviews_set[size:] + neg_reviews_set[size:]
    print(len(test_set),  len(train_set))
    classifier = NaiveBayesClassifier.train(train_set) 
    accuracy = classify.accuracy(classifier, test_set)
    print(accuracy)  
    print (classifier.show_most_informative_features(10))
    return classifier

def pruebaNGRAM(custom_review,classifier):  
    custom_review_tokens = word_tokenize(custom_review)
    custom_review_set = bag_of_all_words(custom_review_tokens)
    print (custom_review) 
    print ('positivo o negativo?',classifier.classify(custom_review_set)) 
    prob_result = classifier.prob_classify(custom_review_set)
    print ('probabilidad para negativo',prob_result.prob("neg")) 
    print ('probabilidad para positivo',prob_result.prob("pos")) 
    

(pos_reviews_set,neg_reviews_set) = DatosNGRAM()
clasifierBOW = clasificadorNGRAM(pos_reviews_set,neg_reviews_set)
texto = "I hated the film. It was a disaster. Poor direction, bad acting."
pruebaNGRAM(texto,clasifierBOW)
texto = "It was a wonderful and amazing movie. I loved it. Best direction, good acting."
pruebaNGRAM(texto,clasifierBOW)

