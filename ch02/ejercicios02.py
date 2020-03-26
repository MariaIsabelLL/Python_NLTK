''' https://www.nltk.org/book/ch02.html
'''

import nltk, re, pprint
import pylab
import decimal
from decimal import *
from nltk.book import *
from nltk import word_tokenize
from nltk.collocations import *
from nltk.corpus import udhr

''' 
4. Read in the texts of the State of the Union addresses, using the 
state_union corpus reader. Count occurrences of men, women, 
and people in each document. 
What has happened to the usage of these words over time?
''' 
from nltk.corpus import state_union
#print(state_union.fileids())

cfdCat= nltk.ConditionalFreqDist((pal,fileid[:4])    
    for fileid in state_union.fileids()
    for pal in ['men', 'women', 'people']
    for w in state_union.words(fileid)
    if w.lower().startswith(pal)
    )

cfdCat.plot()
#cfdCat.plot(conditions=['women'])
#cfdCat.plot(conditions=['men'])
''' 
5. Investigate the holonym-meronym relations for some nouns. 
Remember that there are three kinds of holonym-meronym relation, 
so you need to use: member_meronyms(), part_meronyms(), substance_meronyms(),
 member_holonyms(), part_holonyms(), and substance_holonyms().
''' 
from nltk.corpus import wordnet
print(wordnet.synsets('flower'))

def HoloMero(ss):
    print(ss)
    print('member_meronyms',wordnet.synset(ss).member_meronyms())
    print('part_meronyms',wordnet.synset(ss).part_meronyms())
    print('substance_meronyms',wordnet.synset(ss).substance_meronyms())
    print('member_holonyms',wordnet.synset(ss).member_holonyms())
    print('part_holonyms',wordnet.synset(ss).part_holonyms())
    print('substance_holonyms',wordnet.synset(ss).substance_holonyms())
       
HoloMero('flower.n.01')
HoloMero('tree.n.01')
HoloMero('face.n.01')

''' 
8. Define a conditional frequency distribution over the Names corpus 
that allows you to see which initial letters are more frequent 
for males vs. females
''' 
names = nltk.corpus.names
#print(names.fileids())
#male_names = names.words('male.txt')
#female_names = names.words('female.txt')
#[w for w in male_names if w in female_names]
cfd = nltk.ConditionalFreqDist((fileid, name[0])
        for fileid in names.fileids()
        for name in names.words(fileid))
cfd.plot()

''' 
9. Pick a pair of texts and study the differences between them, 
in terms of vocabulary, vocabulary richness, genre, etc. 
Can you find pairs of words which have quite different 
meanings across the two texts, such as monstrous in Moby Dick 
and in Sense and Sensibility?

''' 

''' 
13. What percentage of noun synsets have no hyponyms? 
You can get all noun synsets using wn.all_synsets('n')
''' 
#wordnet.all_synsets('n')

def porcentaje(wn):
    numTotal=0
    numNotHyp=0   
    for i in wn.all_synsets('n'):
        numTotal += 1
        if not i.hyponyms():
            numNotHyp+= 1
    print('porcentaje:',numNotHyp/numTotal)
       
porcentaje(wordnet)

''' 
14.  Define a function supergloss(s) that takes a synset s 
as its argument and returns a string consisting of the 
concatenation of the definition of s, and the definitions 
of all the hypernyms and hyponyms of s.
'''
def supergloss(s):
    defi= 'definition:'+str(s)+s.definition()
    hyper= ' hypernyms:'
    hypo=' hyponyms:'
    
    for hyp in s.hypernym_paths():
        for syn in hyp:    
            hyper = hyper+str(syn)+',def:'+syn.definition()
        
    for hyp in s.hyponyms():
        hypo = hypo+str(hyp)+',def:'+hyp.definition()
    
    return defi+hyper+hypo

print(supergloss(wordnet.synset('face.n.01')))
print(supergloss(wordnet.synset('tree.n.01')))

''' 
17.  Write a function that finds the 50 most 
frequently occurring words of a text that are not stopwords.
''' 
def mostwords(text,num):
    stopwordsPT = nltk.corpus.stopwords.words('english')
    #print(stopwordsPT)
    fd1 = nltk.FreqDist(w.lower() for w in text if w.isalpha() and w not in stopwordsPT)
    print(str(num)+' palavras mas frecuentes: ',fd1.most_common(num))
    
mostwords(text1,50)

''' 
18.  Write a program to print the 50 most frequent bigrams 
(pairs of adjacent words) of a text, omitting bigrams that 
contain stopwords.
''' 
def mostbig(text,num):
    stopwordsPT = nltk.corpus.stopwords.words('english')
    textList= [w.lower() for w in text if w.isalpha() and w not in stopwordsPT]
    #print(len(textList))
    #print(len(set(textList)))
    finder = BigramCollocationFinder.from_words(textList)
    finder.apply_freq_filter(2)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    collocations = sorted(finder.nbest(bigram_measures.raw_freq, num),reverse=True)
    print(str(num)+' bigramas mas frecuentes: ',collocations)
    
mostbig(text1,50)


''' 
23a.  Zipf's Law: Let f(w) be the frequency of a word w in free text. 
Suppose that all the words of a text are ranked according to 
their frequency, with the most frequent word first. 
Zipf's law states that the frequency of a word type is inversely 
proportional to its rank (i.e. f × r = k, for some constant k). 
For example, the 50th most common word type should occur three times 
as frequently as the 150th most common word type.

    Write a function to process a large text and plot word frequency 
    against word rank using pylab.plot. Do you confirm Zipf's law? 
    (Hint: it helps to use a logarithmic scale). What is going on at 
    the extreme ends of the plotted line?
''' 
def superfreq(text):
    fdist = nltk.FreqDist([w.lower() for w in text])
    keys = fdist.keys()
    #print('keys',keys)
    #print('keys2',fdist)
    freq = []
    rank = []
    freq2 = []
    rank2 = []
    
    for w in keys:
        frequency = fdist[w]
        frequency2 = Decimal.logb(Decimal(fdist[w]))
        freq.append(frequency)
        freq2.append(frequency2)
    
    n = 1 
    for w in keys:
        rank.append(n)
        rank2.append(Decimal.logb(Decimal(n)))
        n = n + 1
    print(n)
    
    pylab.plot(rank, freq)
    pylab.show()
    pylab.plot(rank2, freq2)
    pylab.show()
           
superfreq(text1)

''' 
25. Define a function find_language() that takes a string as 
its argument, and returns a list of languages that have that 
string as a word. Use the udhr corpus and limit your searches 
to files in the Latin-1 encoding.
''' 
def find_language(st):
    listLang=[]
    #print(udhr.fileids())
    for lang in udhr.fileids():
        #print(lang[-7:])
        if lang[-7:]=='-Latin1':
            for word in udhr.words(lang):
                if word == st:
                    listLang.append(lang)
                    break
    print('Lista de Lenguajes de '+st+': ',listLang)
    
find_language("telefone") 
find_language("people") 
find_language("the") 

''' 
28. Use one of the predefined similarity measures to score 
the similarity of each of the following pairs of words. 
Rank the pairs in order of decreasing similarity. 
How close is your ranking to the order given here, 
an order that was established experimentally by 
(Miller & Charles, 1998): car-automobile, gem-jewel, 
journey-voyage, boy-lad, coast-shore, asylum-madhouse, 
magician-wizard, midday-noon, furnace-stove, food-fruit, 
bird-cock, bird-crane, tool-implement, brother-monk, 
lad-brother, crane-implement, journey-car, monk-oracle, 
cemetery-woodland, food-rooster, coast-hill, forest-graveyard, 
shore-woodland, monk-slave, coast-forest, lad-wizard, 
chord-smile, glass-magician, rooster-voyage, noon-string.
''' 
def similarity(word1, word2, wn):
    synset1 = wn.synset(word1 + '.n.01')
    synset2 = wn.synset(word2 + '.n.01')

    return synset1.path_similarity(synset2)

print(similarity('car','automobile',wordnet))
print(similarity('gem','jewel',wordnet))
print(similarity('journey','voyage',wordnet))
print(similarity('boy','lad',wordnet))
print(similarity('coast','shore',wordnet))
print(similarity('asylum','madhouse',wordnet))
print(similarity('magician','wizard',wordnet))
print(similarity('midday','noon',wordnet))
print(similarity('furnace','stove',wordnet))
print(similarity('food','fruit',wordnet))
print(similarity('bird','cock',wordnet))
print(similarity('bird','crane',wordnet))

