
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:28:45 2020
"""

import nltk
nltk.download('book')

'''
CAPITULO 1
'''

from nltk.book import *
print('Texto 9:',text9)
print('Texto 2:',text2)
print('Concordance affection:',text1.concordance('affection'))
print('Similar monstrous:',text1.similar('monstrous'))
print('Common context:',text2.common_contexts(["monstrous", "very"]))

text4.dispersion_plot(['citizens','democracy','freedom'])
text2.dispersion_plot(["Elinor", "Marianne", "Edward", "Willoughby"])

print('Cantiddad de símbolos',len(text3))
print('Cantiddad de palabras',len(set(text3)))
print('Diversidad Léxica',len(set(text3)) / len(text3))
print('Frecuencia de una palabra',text3.count("smote"))
print('Porcentaje del texto que es capturado por una palabra',100 * text4.count('a') / len(text4))

print('Distribución de Frequencia')
fdist5 = FreqDist(text5)
print(fdist5)
print('50 palabras mas frequentes',fdist5.most_common(50))
print(fdist5['ACTION'])
print(fdist5.max())
print(fdist5.freq(3))

fdist5.plot(30, cumulative=True)
fdist5.plot(30, cumulative=False)
print('Palabras que solo se repiten una vez:',fdist5.hapaxes())
print('Palabras de mas de 7 caracteres (long words) repetidas más de 7 veces en el texto',sorted(w for w in set(text5) if len(w) > 7 and fdist5[w] > 7))
print('Ejemplo Bigramas',list(bigrams(['more', 'is', 'said', 'than', 'done'])))

'''print('Palabras secuenciales que están siempre juntas',text1.collocations())'''

print('Ordenar las palabras que comienzan con b',sorted(w for w in set(text5) if w.startswith("b")))

fdist = sorted(FreqDist(w for w in text5 if len(w) == 4))
print('Cantidad de palabras que tienen 4 caracteres ordenadas por orden de frequencia',fdist)
print('Cantidad de palabras que tienen 4 caracteres ordenadas por orden de frequencia',len(fdist))

'''
Write expressions for finding all words in text6 that meet the conditions listed below. The result should be in the form of a list of words: ['word1', 'word2', ...].
Ending in ise
Containing the letter z
Containing the sequence of letters pt
Having all lowercase letters except for an initial capital (i.e., titlecase)
'''
print(sorted(w for w in set(text6) if w.endswith('ise') and 'z' in w and 'pt' in w and w.istitle()))

'''
CAPITULO 2
'''

import nltk
print(nltk.corpus.gutenberg.fileids())
emma = nltk.corpus.gutenberg.words('austen-emma.txt')
print('Cantidad de palabras en el texto Emma',len(emma))

emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
print('Concordancia de surprize',emma.concordance("surprize"))

print('average word length, average sentence length, and the number of times each vocabulary item appears in the text on average (our lexical diversity score).')
for fileid in gutenberg.fileids():
     num_chars = len(gutenberg.raw(fileid))
     num_words = len(gutenberg.words(fileid))
     num_sents = len(gutenberg.sents(fileid))
     num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
     print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)

from nltk.corpus import webtext
for fileid in webtext.fileids():
     print(fileid, webtext.raw(fileid)[:65], '...')

from nltk.corpus import nps_chat
chatroom = nps_chat.posts('10-19-20s_706posts.xml')
print(chatroom[123])

from nltk.corpus import brown
print(brown.categories())
print(brown.words(categories='news'))
print(brown.words(fileids=['cg22']))
print(brown.sents(categories=['news', 'editorial', 'reviews']))
news_text = brown.words(categories='news')
fdist = nltk.FreqDist(w.lower() for w in news_text)
modals = ['can', 'could', 'may', 'might', 'must', 'will']
for m in modals:
     print(m + ':', fdist[m], end=' ')
cfd = nltk.ConditionalFreqDist(
           (genre, word)
           for genre in brown.categories()
           for word in brown.words(categories=genre))
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
cfd.tabulate(conditions=genres, samples=modals)

from nltk.corpus import reuters
reuters.fileids()
reuters.categories()
reuters.categories(['training/9865', 'training/9880'])
reuters.fileids('barley')

from nltk.corpus import inaugural
inaugural.fileids()
[fileid[:4] for fileid in inaugural.fileids()]
    
cfd1 = nltk.ConditionalFreqDist(
           (target, fileid[:4])
           for fileid in inaugural.fileids()
           for w in inaugural.words(fileid)
           for target in ['america', 'citizen']
           if w.lower().startswith(target))
cfd1.plot()    
    
from nltk.corpus import PlaintextCorpusReader
corpus_root = 'D:/maria/PRINCIPAL/Estudios/Maestria UFPI/Cursos Mestrado/TOPICOS/Tarea2/ES' 
wordlists = PlaintextCorpusReader(corpus_root, '.*')
print(wordlists.fileids())
print(wordlists.words('01_es_ciencia.txt'))

names = nltk.corpus.names
print(names.fileids())
male_names = names.words('male.txt')
female_names = names.words('female.txt')
print([w for w in male_names if w in female_names])

cfd = nltk.ConditionalFreqDist(
           (fileid, name[-1])
           for fileid in names.fileids()
           for name in names.words(fileid))
cfd.plot()

from nltk.corpus import stopwords
print(stopwords.words('spanish'))

from nltk.corpus import swadesh
fr2en = swadesh.entries(['es', 'en'])
print(fr2en)
translate = dict(fr2en)
print(translate['perro'])

from nltk.corpus import wordnet as wn
print(wn.synsets('motorcar'))
print(wn.synset('car.n.01').lemma_names())
print(wn.synset('car.n.01').definition())
print(wn.synset('car.n.01').examples())
print(wn.synset('car.n.01').lemmas())
print(wn.lemma('car.n.01.automobile').name())

motorcar = wn.synset('car.n.01')
types_of_motorcar = motorcar.hyponyms()
print(types_of_motorcar)
print(types_of_motorcar[0])
print(wn.synset('ambulance.n.01'))
print(sorted(lemma.name() for synset in types_of_motorcar 
             for lemma in synset.lemmas()))

'''
CAPITULO 3
'''

from urllib import request
from nltk import word_tokenize

url = "http://www.gutenberg.org/files/2554/2554-0.txt"
response = request.urlopen(url)
raw = response.read().decode('utf8')
tokens = word_tokenize(raw)
print('Tokens:',tokens[:10])

from bs4 import BeautifulSoup
url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = request.urlopen(url).read().decode('utf8')
print('HTML:',html[:60])

raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print('Tokens del HTML',tokens)

import re
wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]
print(wordlist)
print([w for w in wordlist if re.search('ed$', w)])

wsj = sorted(set(nltk.corpus.treebank.words()))
print([w for w in wsj if re.search('(ed|ing)$', w)])
print([w for w in wsj if re.search('^[0-9]{4}$', w)])

raw = """Las familias suelen esconder a los niños afectados o los aíslan con los animales"""
tokens = word_tokenize(raw)
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
print([porter.stem(t) for t in tokens])
print([lancaster.stem(t) for t in tokens])

wnl = nltk.WordNetLemmatizer()
print([wnl.lemmatize(t) for t in tokens])

'''
CAPITULO 5
'''
text = word_tokenize("And now for something completely different")
print(nltk.pos_tag(text))

nltk.corpus.brown.tagged_words(tagset='universal')

from nltk.corpus import brown
brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
print('UnigramTagger',unigram_tagger.tag(brown_sents[2007]))
print('Evaluación de exactitud',unigram_tagger.evaluate(brown_tagged_sents))

bigram_tagger = nltk.BigramTagger(brown_tagged_sents,backoff=unigram_tagger)
print('BgramTagger',bigram_tagger.tag(brown_sents[2007]))
print('Evaluación de exactitud',bigram_tagger.evaluate(brown_tagged_sents))
