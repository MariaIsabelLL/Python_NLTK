# IMPORTS
import nltk
import matplotlib
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.collocations import *
from matplotlib import pylab

# FUNCIONES
def estadisticasSimples(corpus,cat,stopwords):
    numChars = 0
    numWords = 0
    numSents = 0
    numVocab = 0
    if stopwords == 0:
        if cat == 0:
            for file in corpus.fileids():
                    numChars += len(corpus.raw(file))
                    numWords += len(corpus.words(file))
                    numSents += len(corpus.sents(file))
                    numVocab += len(set(w.lower()  for w in corpus.words(file)))
            print(round(numChars/numWords), round(numWords/numSents),round(numWords/numVocab))
        else:
            for file in corpus.fileids(categories=[cat]):
                    numChars += len(corpus.raw(file))
                    numWords += len(corpus.words(file))
                    numSents += len(corpus.sents(file))
                    numVocab += len(set(w.lower()  for w in corpus.words(file)))
            print(cat,round(numChars/numWords), round(numWords/numSents),round(numWords/numVocab))
    else:
        if cat == 0:
            for file in corpus.fileids():
                    numChars += len(corpus.raw(file))
                    numWords += len(corpus.words(file))
                    numSents += len(corpus.sents(file))
                    numVocab += len(set(w.lower()  for w in corpus.words(file) if w not in stopwords))
            print(round(numChars/numWords), round(numWords/numSents),round(numWords/numVocab))
        else:
            for file in corpus.fileids(categories=[cat]):
                    numChars += len(corpus.raw(file))
                    numWords += len(corpus.words(file))
                    numSents += len(corpus.sents(file))
                    numVocab += len(set(w.lower()  for w in corpus.words(file) if w not in stopwords))
            print(cat,round(numChars/numWords), round(numWords/numSents),round(numWords/numVocab))
    
def collocations(wordList, num=20,freq_filter=2):
    finder = BigramCollocationFinder.from_words(wordList)
    finder.apply_freq_filter(freq_filter)
    #finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    collocations = sorted(finder.nbest(bigram_measures.raw_freq, num),reverse=True)
    print(collocations)
    
def collocationsScore(wordList,freq_filter=2):   
    finder = BigramCollocationFinder.from_words(wordList)
    finder.apply_freq_filter(freq_filter)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    scored = finder.score_ngrams( bigram_measures.raw_freq)
    #print(len(scored))
    #print(scored)
    for k,v in sorted(finder.ngram_fd.items()):
            print(k,v)
    
def collocationsCond(wordList, word):       
    bigrams = nltk.bigrams(wordList)
    #print(bigrams)
    cfd = nltk.ConditionalFreqDist(bigrams)
    print(cfd[word])
    print(generate_model(cfd, word))

def generate_model(cfdist, word, num=15):
    for i in range(num):
        print(word, end=' ')
        word = cfdist[word].max()

# 1. Construir Corpus texto categorizado
locPT = 'D:/maria/PRINCIPAL/Estudios/Maestria UFPI/Cursos Mestrado/TOPICOS/Tarea2/ES'
corpusPT = CategorizedPlaintextCorpusReader(locPT, '.*\.txt', cat_file="cat.txt")

print(corpusPT.fileids())
print(corpusPT.categories())
print(corpusPT.words(categories='ciencia'))
#print(corpusPT.raw())

vocab = set(w.lower()  for w in corpusPT.words())
print('Tamanho Vocabulario:',len(vocab))
corpusCom = corpusPT.raw()
corpusComList = corpusCom.split()
print('Tamanho Total de palabras:',len(corpusComList))

# 2. Calcular medidas estadisticas simples
'''
Medidas: Tamanho médio das palavras, Tamanho médio das sentenças e Número de vezes que cada
item do vocabulário aparece no	texto em média (escore de diversidade léxica)
'''
print('Tamanho médio das palavras/Tamanho médio das sentenças/Escore de diversidade léxica')
print('Medidas con StopWords de Corpus')
estadisticasSimples(corpusPT,0,0)

print('Medidas con StopWords x Categoria')
for cat in corpusPT.categories():
    estadisticasSimples(corpusPT,cat,0)

# Definicao de stopwords
stopwordsPT = nltk.corpus.stopwords.words('spanish')
#print(stopwordsPT)
vocabSW = set(w.lower() for w in corpusPT.words() if w not in stopwordsPT)
print('Tamanho Vocabulario sin StopWords:',len(vocabSW))
corpusComListSW = [word for word in corpusComList if word not in stopwordsPT]
print('Tamanho Total de palabras sin StopWords:',len(corpusComListSW))

print('Medidas sin StopWords de Corpus')
corpusPTSW = CategorizedPlaintextCorpusReader(locPT, '.*\.txt', cat_file="cat.txt")
estadisticasSimples(corpusPT,0,stopwordsPT)

print('Medidas sin StopWords x Categoria')
for cat in corpusPT.categories():
    corpusPTSW = CategorizedPlaintextCorpusReader(locPT, '.*\.txt', cat_file="cat.txt")
    estadisticasSimples(corpusPT,cat,stopwordsPT)


# 3. Palabras mas frecuentes de corpus y de categoria (collocations e hapaxes)
print('20 Palabras mas frecuentes de corpus')
fd = nltk.FreqDist(w.lower() for w in corpusPT.words())
fd1 = nltk.FreqDist(w.lower() for w in corpusPT.words() if w.isalpha() and w not in stopwordsPT)
#print(fd1)
print(fd1.most_common(20))
print('Grafico Frecuencia Acumulativa de Corpus')
fd1.plot(20, cumulative=True)
print('Grafico Frecuencia de Corpus')
fd1.plot(20, cumulative=False)

listH = fd1.hapaxes()
print('Palabras hapaxes de corpus: ',listH)

listH1=sorted(w for w in set(corpusComListSW) if len(w) > 7 and fd1[w] > 7)
print('Palabras de tamano > 7 que aparecen mas de 7 veces de corpus: ',listH1)

print('Palabras bigramas mas frecuentes de corpus(mas de dos veces)')
#collocations(corpusComListSW, 20,2)
collocationsScore(corpusComListSW, 2)
collocationsCond(corpusComListSW, 'América')

print('20 Palabras mas frecuentes x categoria')
for cat in corpusPT.categories():
    fdCat = nltk.FreqDist(w.lower() for w in corpusPT.words(categories=cat) if w.isalpha() and w not in stopwordsPT)
    print(cat,fdCat.most_common(20))
    fdCat.plot(20, cumulative=False)
    listHCat = fdCat.hapaxes()
    print('Palabras hapaxes: ',cat,listHCat)
    corpusComListSWCat = [word for word in (corpusPT.raw(categories=cat)).split() if word not in stopwordsPT]
    listH1Cat=sorted(w for w in set(corpusComListSWCat) if len(w) > 7 and fd1[w] > 7)
    print('Palabras de tamano > 7 que aparecen mas de 7 veces de corpus: ',cat, listH1Cat)
    print('20 Palabras bigramas mas frecuentes de corpus por cat: ', cat)
    #collocations(corpusComListSWCat, 20,2)
    collocationsScore(corpusComListSWCat, 2)

# 4. Calcular Distribucion Frecuencia Condicional entre palavras y categorias
print('Distribucion Frecuencia Condicional ')

cfdCat= nltk.ConditionalFreqDist((cat, pal)
    for cat in corpusPT.categories()
    for pal in corpusPT.words(categories=cat)
                                 )
cfdCat.plot()
#print(cfdCat.conditions())
#cfdCat.plot(conditions=['ciencia','internacional'])
print(cfdCat['internacional'].most_common(20))
print("['tecnologia']['redes']:",cfdCat['tecnologia']['redes'])


print('Distribucion Frecuencia Condicional - tamanho de palabras')
cfdCat2= nltk.ConditionalFreqDist((cat, len(pal))
    for cat in corpusPT.categories()
    for pal in corpusPT.words(categories=cat)  
    )
cfdCat2.plot()
cfdCat2.tabulate(conditions=['ciencia', 'internacional'],samples=range(10), cumulative=True)

print('Distribucion Frecuencia Condicional para palabras de tamano > 7 que aparecen mas de 7 veces de corpus')
cfdCat3= nltk.ConditionalFreqDist((cat, pal)
    for cat in corpusPT.categories()
    for pal in corpusPT.words(categories=cat) if pal in listH1  
    )
cfdCat3.plot()

