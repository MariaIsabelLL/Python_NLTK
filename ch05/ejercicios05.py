''' https://www.nltk.org/book/ch05.html

'''
import nltk
nltk.download('mac_morpho')
nltk.download('cess_esp')
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import mac_morpho
import datetime

''' 
8. Create a dictionary e, to represent a single lexical entry 
for some word of your choice. Define keys like headword, 
part-of-speech, sense, and example, and assign them suitable values.

''' 
word = "currently"
text = word_tokenize(word)
f = dict(nltk.pos_tag(text))
print(wordnet.synsets(word))
e = {}
e['headword']= word
e['part-of-speech']= f['currently']
e['sense']= wordnet.synset('presently.r.02').definition()
e['example']= wordnet.synset('presently.r.02').examples()
print(e)

''' 
9. Satisfy yourself that there are restrictions on the 
distribution of go and went, in the sense that they cannot 
be freely interchanged in the kinds of contexts illustrated
 in (3d) in 7.
''' 
f = dict(nltk.pos_tag(word_tokenize('went')))
print(f)
f = dict(nltk.pos_tag(word_tokenize('go')))
print(f)

f = dict(nltk.pos_tag(word_tokenize('We went on the excursion yesterday')))
print(f)

f = dict(nltk.pos_tag(word_tokenize('We go on the excursion yesterday')))
print(f)

''' 
13. We can use a dictionary to specify the values to be 
substituted into a formatting string. Read 
Python's library documentation for formatting s
trings http://docs.python.org/lib/typesseq-strings.html 
and use this method to display today's date in two 
different formats.
''' 

d = datetime.datetime.today()
print(d)
g = datetime.datetime(2010, 7, 4, 12, 15, 58)
print('{:%Y/%m/%d %H:%M:%S}'.format(g))
print('Formato 1: ','{:%Y/%m/%d %H:%M:%S}'.format(d))
print('Formato 2: ','{:%d/%m/%Y %H:%M:%S}'.format(d))

''' 
14. Use sorted() and set() to get a sorted list of tags
 used in the Brown corpus, removing duplicates.
''' 
text1 = nltk.corpus.brown.tagged_words()
print('Brown Tag Word' ,text1)
diccionarioBrownTag = dict(text1)
print('Diccionario Brown Tag Word' ,diccionarioBrownTag)
soloTag = set(diccionarioBrownTag.values())
print(sorted(soloTag))

''' 
18. Generate some statistics for tagged data to answer 
the following questions:

    What proportion of word types are always assigned 
    the same part-of-speech tag?
    How many words are ambiguous, in the sense that 
    they appear with at least two tags?
    What percentage of word tokens in the Brown Corpus 
    involve these ambiguous words?
''' 
textBrownTag = nltk.corpus.brown.tagged_words(tagset='universal')
#textBrownTag = nltk.corpus.brown.tagged_words()

print('Total words Brown Tag',len(textBrownTag))
print('Total words Brown Tag(set)',len(set(textBrownTag)))
dataCondFreqD = nltk.ConditionalFreqDist((word.lower(), tag)
                                 for (word, tag) in textBrownTag)

#print(len(data.conditions()))
#data.plot(conditions=['the'])
#print(len(data['the']))
print(dataCondFreqD['the'].most_common())
print(dataCondFreqD['flies'].most_common())
print(dataCondFreqD['absolutely'].most_common())
print(dataCondFreqD['definitely'].most_common())
print(dataCondFreqD['like'].most_common())

countA=0
countNotA=0
wordsA=[]
''' 
for word in sorted(dataCondFreqD.conditions()):
    if len(dataCondFreqD[word]) > 1:
        countA+=1
        wordsA.append(word)
    if len(dataCondFreqD[word]) == 1:
        countNotA+=1
        
print('total de palavras no ambiguas:',countNotA)
print('total de palavras ambiguas:',countA)
''' 
porc = countA / len(nltk.corpus.brown.words())
print(len(nltk.corpus.brown.words()))
print(porc*100)


totalBrownWord = nltk.corpus.brown.words()
totalBrownSet = set(nltk.corpus.brown.words())
print('Total words Brown',len(totalBrownWord))
print('Total words Brown (set)',len(totalBrownSet))
#print(nltk.corpus.brown.words())

wordsAmBrown = [word for word in totalBrownSet if word in wordsA]
print('Total words ambiguas en Brown',len(wordsAmBrown))
porc = len(wordsAmBrown) / len(totalBrownSet)
print('porc de palabras ambiguas en Brown:',porc*100,'%')

        
''' 
20. Write code to search the Brown Corpus for particular words 
and phrases according to tags, to answer the following questions:

    Produce an alphabetically sorted list of the distinct words 
    tagged as MD.
    Identify words that can be plural nouns or third person 
    singular verbs (e.g. deals, flies).
    Identify three-word prepositional phrases of the 
    form IN + DET + NN (eg. in the lab).
    What is the ratio of masculine to feminine pronouns?
''' 
print('dataCondFreqD',dataCondFreqD.conditions())

wordsMD = []
wordsPN = []
for word in sorted(dataCondFreqD.conditions()):
    if 'MD' in dataCondFreqD[word]:
        wordsMD.append(word)
    if 'NNS' in dataCondFreqD[word] and 'VBZ' in dataCondFreqD[word]:
        wordsPN.append(word)
        
#print('words tagged as MD:',sorted(wordsMD))
#print('plural nouns or third person singular verbs:',sorted(wordsPN))
               
#print('dict',f)  
#print('dict',nltk.corpus.brown.words()) 
frases = []
frase = []
count1 = 0

for (word, tag) in textBrownTag:
    if tag == 'ADP' and count1==0:
        frase.append(word)
        count1=1
        #print('IN',word)
    elif tag == 'DET' and count1==1:
        frase.append(word)
        count1=2
        #print('DET',frase)
    elif tag == 'NOUN' and count1==2:
        frase.append(word)
        count1=3
        #print('NN',frase)
    else:
        count1=0
        frase = []
    if count1==3:
        frases.append(frase)
        
#print('IN + DET + NN',frases)

masculino = len(dataCondFreqD['he']) 
femenino = len(dataCondFreqD['she'])
print(masculino)
print(femenino)
print(dataCondFreqD['he'].most_common())
print(dataCondFreqD['she'].most_common())

dataCondFreqD.plot(conditions=['he'])
dataCondFreqD.plot(conditions=['she'])
#
masculino = [word for word in totalBrownWord if word == 'he']
femenino = [word for word in totalBrownWord if word == 'she']
print('ratio of masculine to feminine pronouns',len(masculino)/len(femenino))


''' 
21. In 3.1 we saw a table involving frequency 
counts for the verbs adore, love, like, prefer 
and preceding qualifiers absolutely and definitely. 
Investigate the full range of adverbs that appear
 before these four verbs.
''' 

count2= 0
listVerb = ['adore','love','like','prefer']
listAdverb  = []
palabraAnt = ''
for (word, tag) in textBrownTag:
    if tag == 'ADV' and count2==0:
        palabraAnt=word
        count2=1
    elif word in listVerb and tag == 'VERB' and count2==1:
        count2=2
    else:
        count2=0
    if count2==2 and palabraAnt not in listAdverb:
        listAdverb.append(palabraAnt)
        palabraAnt = ''
           
#print('listAdverb',listAdverb)

for ((a,b), (c,d)) in nltk.bigrams(textBrownTag):
    if b == 'ADV' and d=='VERB' and c in listVerb:
        print((a,b), (c,d))   

''' 
30. Preprocess the Brown News data by replacing low 
frequency words with UNK, but leaving the tags untouched. 
Now train and evaluate a bigram tagger on this data. 
How much does this help? What is the contribution of the 
unigram tagger and default tagger now?
''' 


def tagTexto(ws):
    size = int(len(ws) * 0.9)
    train_sents = ws[:size]
    test_sents = ws[size:]

    t0 = nltk.DefaultTagger('NN')
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)

    print('BigramTagger con backoff',t2.evaluate(test_sents))

    t3 = nltk.BigramTagger(train_sents)
    print('BigramTagger sin backoff',t3.evaluate(test_sents))
    
    return t2


textoBrownTagWordNew = nltk.corpus.brown.tagged_words(categories='news', tagset='universal')
fdTag = nltk.FreqDist(tag for (word, tag) in textoBrownTagWordNew)
print('tags',fdTag.most_common())
fdTag0 = nltk.FreqDist(word for (word, tag) in textoBrownTagWordNew)
#print('tags0',fdTag0.most_common())

textoBrownTagSent = nltk.corpus.brown.tagged_sents(categories='news', tagset='universal')
#print(textoBrownTagNew)
#print(textoBrownTagWordNew)   
#fdTag1 = nltk.FreqDist(tag for (word, tag) in (for k in textoBrownTagNew))
fdTag1 = nltk.FreqDist(tag for k in textoBrownTagSent for (word, tag) in k)
print('tags1 TAG',fdTag1.most_common())
tagTexto(textoBrownTagSent)

textoBrownNew = nltk.corpus.brown.words(categories='news')
fdWord = nltk.FreqDist(textoBrownNew)
listLowFreq = list(w for w in textoBrownNew if fdWord[w]<=3)

#fdTag2 = nltk.FreqDist(tag for (word, tag) in i for i in textoBrownTagNew)
#print(fdTag2.most_common())

#for (word, tag) in textoBrownTagWordNew:
#    if word in listLowFreq:
#        word = 'UNK'
textoBrownTagSentNew = []

for i in textoBrownTagSent:
    sentNew = []
    for (word, tag) in i:
        if word in listLowFreq:
            word = 'UNK'
        sentNew.append((word, tag))
    textoBrownTagSentNew.append(sentNew)
    
            
#print('segundo',textoBrownTagSentNew)
fdTag2 = nltk.FreqDist(tag for m in textoBrownTagSentNew for (word, tag) in m)
print('tags2 TAG',fdTag2.most_common())

fdTag3 = nltk.FreqDist(word for m in textoBrownTagSentNew for (word, tag) in m)
#print('tags2 WORD',fdTag3.most_common())

tagTexto(textoBrownTagSentNew)


''' 
1.Estender	o	exemplo	 dos	etiquetadores	para	
TrigramTagger e	analisar	a	precisao	do	modelo	
''' 

treino = mac_morpho.tagged_sents()[1000:]
teste = mac_morpho.tagged_sents()[:1000]
etiq0 = nltk.DefaultTagger('N')
etiq1 = nltk.UnigramTagger(treino, backoff=etiq0)
print('UnigramTagger',etiq1.evaluate(teste))
etiq2 = nltk.BigramTagger(treino,  backoff=etiq1)
print('BigramTagger',etiq2.evaluate(teste))
etiq3 = nltk.TrigramTagger(treino,  backoff=etiq2)
print('TrigramTagger',etiq3.evaluate(teste))

doc = open('textoPT.txt',encoding='utf8')
raw = doc.read()

#texto = nltk.word_tokenize('O  mundo atual possui diversos idiomas.')
texto = nltk.word_tokenize(raw)
#print('etiq2', etiq2.tag(texto))
#print('etiq3', etiq3.tag(texto))


''' 
2. Implementar	 a	 tecnica	de	validacao	10-fold	
cross-validation	e	analisar	a	precisao	dos	
modelos.	Discutir	os	resultados.	
''' 

# scikit-learn k-fold cross-validation
from numpy import array
from sklearn.model_selection import KFold
data = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
data2 = mac_morpho.tagged_sents()
#print(data2[1])
#print(data2[2])
# prepare cross validation
kfold = KFold(10, True, 1)
# enumerate splits

count5=0
for train, test in kfold.split(data2):
    train_sents1 = []
    test_sents1 = []
    count5+=1
    print(count5)
    #print(train.size)
    #print(test.size)
    for i in train:
        #print(i)
        train_sents1.append(data2[i])
    for i in test:
        test_sents1.append(data2[i])
    etiq1 = nltk.UnigramTagger(train_sents1, backoff=etiq0)
    print('UnigramTagger',etiq1.evaluate(test_sents1))
    etiq2 = nltk.BigramTagger(train_sents1,  backoff=etiq1)
    print('BigramTagger',etiq2.evaluate(test_sents1))
    etiq3 = nltk.TrigramTagger(train_sents1,  backoff=etiq2)
    print('TrigramTagger',etiq3.evaluate(test_sents1))
    #print(data2[train])
    #print('train: %s, test: %s' % (data2[train], data[test]))

print(len(train_sents1))

''' 
3. Ler	sobre	Etiquetagem	baseada	em	
transformacoes	(do	ingles:	Transformation-
Based	Tagging). 	Ver	 secao	6,	disponivel	em:	
http://www.nltk.org/book/ch05.html	
''' 
''' 
EN ESPAÑOL
''' 
from nltk.corpus import cess_esp as cess

cess_sents = cess.tagged_sents()
print(cess_sents)
etiq3 = tagTexto(cess_sents)

doc = open('textoES.txt',encoding='utf8')
raw = doc.read()
texto = nltk.word_tokenize(raw)
print('etiq2 ESP', etiq3.tag(texto))

from nltk.tag.stanford import StanfordPOSTagger
