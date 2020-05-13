
"""
Created on Fri Mar 27 09:50:08 2020

"""
import tweepy 
from tweepy import OAuthHandler
import re
import json

import nltk
from nltk import bigrams
from nltk import word_tokenize
from nltk.stem import SnowballStemmer

from pickle import dump
from pickle import load
from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime, date, time, timedelta
from collections import Counter

from tweepy import Stream
from tweepy import Cursor
from tweepy.streaming import StreamListener
import csv

stopwords = nltk.corpus.stopwords.words('spanish')
stopwords.append('----')
stopwords.append('---')
stopwords.append('--')
stopwords.append(':')
stopwords.append(',')
stopwords.append('!')
stopwords.append('/')
stopwords.append('.')
stopwords.append('?')
stopwords.append('"')
stopwords.append('>')
stopwords.append('…')

#Credenciales del Twitter API
access_key = "XXXXXX"
access_secret = "XXXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"

'''Método de Autenticación para conectarse a twitter'''
def autenticacion():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api

'''leer el timeline de nuestra cuenta de Twitter '''
def get_my_tweets():      
    api = autenticacion()
    public_tweets = api.home_timeline(10)
    for tweet in public_tweets:
        print (tweet.text)

#get_my_tweets()

'''obtener los usuarios a los cuales seguimos'''
def get_my_friends():      
    api = autenticacion()
    friends = api.friends()
    for friend in friends:
        print (friend.name)

#get_my_friends()

'''obtener información de un usuario'''
def get_last_tweets_x_user(screen_name):
    api = autenticacion()
    tweetCount = 10
    
    print("Getting data for " + screen_name)
    item = api.get_user(screen_name)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("tweets_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))
    
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
      print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))
      
    resultado = api.user_timeline(id=screen_name, count=tweetCount)
    for tweet in resultado:
        print(tweet.text)

#get_last_tweets_x_user("@realDonaldTrump")      
  
'''Obtener los hashtags mas usados de un usuario'''
def get_most_common_hashtags_x_user(screen_name):
       
    api = autenticacion()
    hashtags = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=30)
    for status in Cursor(api.user_timeline, id=screen_name).items():
      tweet_count += 1
      if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
          for ent in entities["hashtags"]:
            if ent is not None:
              if "text" in ent:
                hashtag = ent["text"]
                if hashtag is not None:
                  hashtags.append(hashtag)
      if status.created_at < end_date:
        break
    
    print("Most used hashtags:")
    for item, count in Counter(hashtags).most_common(10):
      print(item + "\t" + str(count))

    print("All done. Processed " + str(tweet_count) + " tweets.")
    
#get_most_common_hashtags_x_user("@canalN_")     
#get_most_common_hashtags_x_user("@realDonaldTrump") 

#Remover los caracteres no imprimibles y los saltos de línea del texto del tweet
def strip_undesired_chars(tweet):
    stripped_tweet = tweet.replace('\n', ' ').replace('\r', '')
    char_list = [stripped_tweet[j] for j in range(len(stripped_tweet)) if ord(stripped_tweet[j]) in range(65536)]
    stripped_tweet=''
    for j in char_list:
        stripped_tweet=stripped_tweet+j
    return stripped_tweet

'''Salvar tweets a csv'''
def save_tweets_x_user(screen_name):
    #Este método solo tiene permitido descargar máximo los ultimos 3240 tweets del usuario
    #Especificar aquí durante las pruebas un número entre 200 y 3240
    limit_number = 500
    api = autenticacion()
    alltweets = []   
        
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    
    while len(new_tweets) > 0 and len(alltweets) <= limit_number:
        new_tweets = api.user_timeline(screen_name = screen_name,count=50,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(str(len(alltweets)) + " tweets descargados hasta el momento")
    
    alltweets.pop(215)
    outtweets = [(tweet.id_str, tweet.created_at, strip_undesired_chars(tweet.text),tweet.retweet_count,str(tweet.favorite_count)+'') 
                for tweet in alltweets]
    
    with open('%s_tweets.csv' % screen_name, "w", encoding="utf-8", newline='') as f:       
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['id','created_at','text','retweet_count','favorite_count'''])
        writer.writerows(outtweets)    
    pass

#save_tweets_x_user("@canalN_") 
    
""" Obtener tweets en línea"""
#class MyListener(StreamListener):
#    def on_data(self,data):
#        print("")
#        try:            
#            with open("vizcarra08042020.json","a") as f:
#                f.write(data)
#                return True
#        except BaseException as e:
#            print(e)
#            return True
#
#    def on_error(self,status):
#        print(status)
#        return True
# 
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_key, access_secret)
#twitter_stream = Stream(auth,MyListener())
#twitter_stream.filter(track=["vizcarra"], languages=['es'] )  


""" tokenizar tweets"""
def preprocess(s):
    emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
        
    regex_str =[emoticons_str,
                r'<[^>]+>' , #HTML tags
                r'(?:@[\w_]+)' , #@-Mención
                r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" , #Hash-tags
                r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', #URLs
                r'(?:[\w_]+)' , #Otras Palabras
                r'(?:\S)' #Otras Palabras
                ]    
    
    tokens_re = re.compile (r'('+'|'.join(regex_str)+')' ,re.VERBOSE | re.IGNORECASE)
    tokens = tokens_re.findall(s)
    return tokens

tweet = ' RT @amla: sólo un ejemplo! :D http://example.com #NLP en Perú :-)'
print(word_tokenize(tweet))
print(preprocess(tweet))


'''Obtener tokens de los tweets'''
def tokens_text(arc):
    count=0
    tweets_tokens_all=[]
    with open (arc ,"r") as f:  
        count_all = Counter()
        for line in f:        
            count= count + 1              
            if not line.isspace():
                tweet = json.loads(line)
                full_text = tweet["text"]
                
                if "quoted_status" in tweet:                
                    tweet_quoted= tweet["quoted_status"]
                    if "extended_tweet" in tweet_quoted: 
                        tweet_extended = tweet_quoted["extended_tweet"]
                        if "full_text" in tweet_extended: 
                            full_text = tweet_extended["full_text"]
                            
                "#Crea una lista con todos los términos sin stop"
                terms_all = [term for term in preprocess(full_text) 
                            if term not in stopwords]
                
                "#Actualiza el contador"
                count_all.update(terms_all)
                tweets_tokens_all.extend(terms_all)
             
    print("total de tweets", count)
    
    "#Imprime las primeras 5 palabras con mayor frecuencia"
    print("primeras 5 palabras con mayor frecuencia",count_all.most_common(5))
    return tweets_tokens_all

#tokens_text("vizcarra08042020.json")
   
'''Obtener estadísticas de los tweets'''
def get_estadisticas(tweets_tokens_all):

    # Crea una lista con todos los #hash-tags
    terms_hash = [term for term in tweets_tokens_all if term.startswith('#')]
    print('Distribución de Frequencia de HashTags')
    fdist = nltk.FreqDist(terms_hash)
    print('50 palabras mas frequentes',fdist.most_common(50))
    fdist.plot(30, cumulative=False)
    
    # Cuenta las palabras unicamente, sin #hashtags ni @-menciones
    terms_only = [term for term in tweets_tokens_all if term not in stopwords
                   and not term.startswith(('#', '@'))]
    print('Distribución de Frequencia de Todas las Palabras')
    fdist_todos = nltk.FreqDist(terms_only)
    print('50 palabras mas frequentes',fdist_todos.most_common(50))
    fdist_todos.plot(30, cumulative=False)    
                                           
    # Cuenta los terminos solo una vez en cada tweet.
    terms_single = set(tweets_tokens_all)
    print(len(terms_single))
    
    terms_bigram = bigrams(tweets_tokens_all)
    print("BIGRAMAS",terms_bigram) 

#get_estadisticas(tokens_text("vizcarra08042020.json"))

