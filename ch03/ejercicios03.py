''' https://www.nltk.org/book/ch03.html

'''
import nltk
from urllib import request
from bs4 import BeautifulSoup
from nltk.corpus import names
from nltk import word_tokenize
from nltk.corpus import words
import re

# loads an list full of names
options = names.fileids()
name_options = [names.words(f) for f in options]
# flattens the list
name_options = [item for sublist in name_options for item in sublist]

''' 
8. Write a utility function that takes a URL as its argument, 
and returns the contents of the URL, with all HTML markup removed. 
Use from urllib import request and then 
request.urlopen('http://nltk.org/').read().decode('utf8') 
to access the contents of the URL.
''' 
def contentURL(url):
    contenido = request.urlopen(url).read().decode('utf8') 
    soup = BeautifulSoup(contenido, "lxml")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    tokens = word_tokenize(text)
    return tokens

print(contentURL('http://nltk.org/'))

''' 
9. Save some text into a file corpus.txt. Define a function load(f) 
that reads from the file named in its sole argument, and returns a 
string containing the text of the file.

    Use nltk.regexp_tokenize() to create a tokenizer that tokenizes 
    the various kinds of punctuation in this text. Use one multi-line 
    regular expression, with inline comments, using the verbose flag (?x).
    Use nltk.regexp_tokenize() to create a tokenizer that tokenizes 
    the following kinds of expression: monetary amounts; dates; 
    names of people and organizations.

''' 
def load(f):
    doc = open(f,encoding='utf8')
    #doc = open(f,encoding="ISO-8859-1")
    raw = doc.read()
    return raw
    
def regexp(raw):    
    #kinds of punctuation
    pattern = r'''(?x)    # set flag to allow verbose regexps
    \W 						# searches for non-alphanumeric characters.
	'''
    tokPunc = nltk.regexp_tokenize(raw,pattern)
    print('non-alphanumeric characters:',tokPunc)
    
    #monetary amounts
    pattern = r'''(?x)    # set flag to allow verbose regexps
    \$\d+\.\d+  # currency e.g. $12.40
    '''
    tokMon = nltk.regexp_tokenize(raw,pattern)
    print('currency:',tokMon)
    
    #dates
    pattern = r'''(?x)    # set flag to allow verbose regexps
    \d\d\/\d\d\/\d\d\d\d  # date formato dd/mm/yyyy
    '''
    tokMon = nltk.regexp_tokenize(raw,pattern)
    print('data formato dd/mm/yyyy:',tokMon)
    
    #names of people 
    pattern = r'''(?x)    # set flag to allow verbose regexps
    [A-Z][a-z]+	       # names of people 
    '''
    raw_matches = nltk.regexp_tokenize(raw, pattern)
    name_matches = [match for match in raw_matches if match in name_options]
    print('names of people',name_matches)
    return raw
    
#print(load('textoEN2.txt'))
regexp(load('textoEN.txt'))

''' 
13. What is the difference between calling split on a string with 
no argument or with ' ' as the argument, e.g. sent.split() versus 
sent.split(' ')? What happens when the string being split 
contains tab characters, consecutive space characters, or a sequence 
of tabs and spaces? (In IDLE you will need to use '\t' to enter a 
tab character.)
''' 
texto = load('textoEN.txt')
#print(texto.split())
print(texto.split(' '))


''' 
14.  Create a variable words containing a list of words. 
Experiment with words.sort() and sorted(words). 
What is the difference?''' 

wordsPrueba = ['Maria','Rosa','ventana','mueble','termo','Ana','palabra','xenofobia','bobo']
print(sorted(wordsPrueba))
print(wordsPrueba)
wordsPrueba.sort()
print(wordsPrueba)

''' 
18. Read in some text from a corpus, tokenize it, and print the 
list of all wh-word types that occur. (wh-words in English are 
used in questions, relative clauses and exclamations: who, which, 
what, and so on.) Print them in order. Are any words duplicated 
in this list, because of the presence of case distinctions or 
punctuation?
''' 

def allword(url,wordIni):
    texto = load(url)
    token = word_tokenize(texto)
    #listWord = [w for w in token if re.search('^'+wordIni,w)]
    listWord = []
    for w in token:
        if re.search('^'+wordIni,w.lower()) and w not in listWord:
            listWord.append(w)
            
    print(sorted(listWord))
    return listWord

allword('textoEN.txt','wh')

''' 
20. Write code to access a favorite webpage and extract some text 
from it. For example, access a weather site and extract the forecast
 top temperature for your town or city today.
''' 
def has_title(tag):
    return tag.has_attr('title')

def contentURL2(url,frase):
    contenido = request.urlopen(url).read()#.decode('utf8') 
    #soup = BeautifulSoup(contenido, "lxml")
    soup = BeautifulSoup(contenido, 'html.parser')
    #texto1 = soup.find_all('title',string=re.compile(frase))
    #texto1 = soup.find_all('img',attrs={'title':'WhatsApp'})
    #listImg = soup.find_all('img')
    listImg = soup.find_all(has_title)
    listFrase = []
    for w in listImg:
        desc=w['title']
        if frase.lower() in desc.lower() and desc not in listFrase: 
            listFrase.append(desc)
            
    return listFrase

print('Noticias con la palabra Youtube',contentURL2('https://larepublica.pe/','Youtube'))
print('Noticias con la palabra Fujimorismo',contentURL2('https://larepublica.pe/','Fujimorismo'))


''' 
21. Write a function unknown() that takes a URL as its argument, 
and returns a list of unknown words that occur on that webpage. 
In order to do this, extract all substrings consisting of lowercase 
letters (using re.findall()) and remove any items from this set 
that occur in the Words Corpus (nltk.corpus.words). 
Try to categorize these words manually and discuss your findings.
''' 
def unknown(url,wordsCorpus):
    listTexto = contentURL(url)
    texto = ' '.join(listTexto)
    listLow = re.findall("[a-z]+", texto)
    #print('solo minusculas',listLow)
    #print('palabras de word corpus',wordsCorpus)
    listWord = []
    for w in listLow:
        if w not in wordsCorpus and w not in listWord:
            listWord.append(w)
                      
    return listWord

listWordsCorpus = words.words()
listUn= unknown('http://nltk.org/',listWordsCorpus)
print('palabras desconocidas',listUn)

''' 
30. Use the Porter Stemmer to normalize some tokenized text, 
calling the stemmer on each word. Do the same thing with the 
Lancaster Stemmer and see if you observe any differences.
''' 
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
texto = load('textoEN2.txt')
tokTexto = word_tokenize(texto)
print([porter.stem(t) for t in tokTexto])
print([lancaster.stem(t) for t in tokTexto])

''' En espaol
'''
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')
stemmer.stem('cuando')
text = load('textoES.txt')
stemmed_text = [stemmer.stem(i) for i in word_tokenize(text)]
print(stemmed_text)

''' En Portugues
'''
stemmer2 = SnowballStemmer('portuguese')
stemmer2.stem('quando')
text2 = load('textoPT.txt')
stemmed_text2 = [stemmer2.stem(i) for i in word_tokenize(text2)]
print(stemmed_text2)


''' 
43. With the help of a multilingual corpus such as the 
Universal Declaration of Human Rights Corpus (nltk.corpus.udhr), 
and NLTK's frequency distribution and rank correlation 
functionality (nltk.FreqDist, nltk.spearman_correlation), 
develop a system that guesses the language of a previously 
unseen text. For simplicity, work with a single character 
encoding and just a few languages.
'''
from nltk.corpus import udhr
from nltk.metrics.spearman import *

def language(texto):
    
    #fd = nltk.FreqDist(texto)
    fd = nltk.FreqDist(word_tokenize(texto))
    #print(list(fd))
    #print(fd.most_common(50))
    correlationMax = -10000
    langFinal= '-Latin1'
    
    for lang in udhr.fileids():
        if lang[-7:]=='-Latin1':
            fdu = nltk.FreqDist(word_tokenize(udhr.raw(lang)))
            #fdu = nltk.FreqDist(udhr.raw(lang))
            correlation = nltk.spearman_correlation(
                    list(ranks_from_sequence(fd)),
                    list(ranks_from_sequence(fdu)))
            #print(fdu.most_common(50))
            #print(lang,correlation)
            if correlation > correlationMax:
                langFinal = lang
                correlationMax = correlation
                      
    return langFinal+',corr:'+str(correlationMax)

print(language(load('textoPT.txt')))
print(language(load('textoEN.txt')))
print(language(load('textoES.txt')))

