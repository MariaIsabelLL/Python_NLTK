   import nltk

# Corpus texto simples
from nltk.corpus import PlaintextCorpusReader
loc = '/Users/rmoura/nltk_data/corpora/rai/textoSimples/'
corpus1 = PlaintextCorpusReader(loc, '.*\.txt')
print(corpus1.fileids())
print(corpus1.sents())
print(corpus1.words())

# Corpus texto etiquetado
from nltk.corpus.reader.tagged import TaggedCorpusReader
loc = '/Users/rmoura/nltk_data/corpora/rai/textoEtiquetas/'
corpus2 = TaggedCorpusReader(loc, '.*\.txt')
print(corpus2.fileids())
print(corpus2.words())
print("Palavras etiquetadas: ", corpus2.tagged_words())
print(corpus2.tagged_words('003.txt'))
print("Sentencas diretas:")
for s in corpus2.sents():
    print(' '.join(s))

from nltk.corpus.reader import CategorizedPlaintextCorpusReader
loc = '/Users/rmoura/nltk_data/corpora/rai/textoCategorias/'
corpus3 = CategorizedPlaintextCorpusReader(loc, '.*\.txt', cat_file="categorias.txt")
print(corpus3.fileids())
print(corpus3.categories())
print(corpus3.words(categories='brasnam'))

# Definicao de stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
fd = nltk.FreqDist(w.lower() for w in corpus3.words())
fd1 = nltk.FreqDist(w.lower() for w in corpus3.words()
                    if w.isalpha() and w not in stopwords)
   
