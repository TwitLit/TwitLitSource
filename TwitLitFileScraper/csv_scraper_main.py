"""
Author: Nick Caravias
Email: ngc005@bucknell.edu
Instructor: Dr. Christian Howard-Sukhil

Twit Lit Project Fall 2020
Digital Humanities @ Bucknell University
"""
import csv
import nltk
import re
import os

from nltk.tokenize import word_tokenize
from nltk.collocations import *
from langdetect import detect

#from collation import *


'''--------------------------Tweet Text Analytics---------------------------'''
'''
Cleans the csv file for NLP using NLTK. Need to use nested for loop or eqivolent 
runtime algorithm to see each work in order to tokenize for NLP. Other 
analytics are also included in this method when each tweet field is examined in
order to reduce runtime.


@return a tokenized list of words from a csv file
@param a csv file
'''

def tokenize_csv(file):
  tokens = []
  global hashtags
  global mentions
  global favorites
  global retweets
  
  with open(file, newline='') as f:
    reader = csv.reader(f)

    for line in reader:
      #removes the non tweet information from the csv file
      line = line[1:]
      
      #look at each word
      for field in line:
        
        
        
        #see if the tweet contains hashtags
        if '#' in field:
          find_hashtag(field, hashtags)
        
        #see if the tweet contains mentions
        if '@' in field:
          mentions['tweets with mentions'] += 1
         
          field_num_mentions = field.count('@')
          
          mentions['total mentions'] += field_num_mentions
        
        if '@' not in field:
          mentions['tweets without mentions'] += 1
        
        #regex to clean 
        field = re.sub('\W+',' ', field)
        
        tokens += word_tokenize(field)
                
  return tokens


'''
Finds the ratio of tweets with mentions to tweets without mentions

@param dictionary holding mentions data
@return tweets with mentions / tweets without mentions
'''
def get_mentions_ratio(dictionary):
  with_tweets = dictionary['tweets with mentions']
  without_tweets = dictionary['tweets without mentions']
  
  if without_tweets == 0:
    return 'N/A'

  ratio = with_tweets / without_tweets
  
  return ratio

'''
Finds the amount of mentions per tweet

@param dictionary holding mentions data
@return total mentions / total tweets
'''
def get_mentions_per_tweet(dictionary):
  
  mentions = dictionary['total mentions']
  tweets = dictionary['tweets with mentions'] + dictionary['tweets without mentions']
  
  if tweets == 0:
    return 'N/A'
  
  mentions_per_tweet = mentions / tweets
  
  return mentions_per_tweet

'''
Finds the top hashtags in the dictionary

@param dictionary: the dictionary to look at
@param num: the number of desired hashtags
@return top_hashtags: the top hashtags as a list
'''
def get_top_hashtags(dictionary, num):
  #check if there are no tweets
  res = not bool(dictionary)
  if res == True:
    return 'No hashtags in file'

  arr = [[] for i in range(num)]
  counter = 0
  
  top_hashtags = []
  
  for i in range(num):
    m = max(dictionary, key=hashtags.get)
    
    top_hashtags.append(m)
    dictionary[m] = 0
  
    
  return top_hashtags




def find_hashtag(field, dictionary):
  #find the hastags in the tweet field
  tags = [i for i, x in enumerate(field) if x  == '#']
  
  #need to find each hashtag in the field so interate through tags
  for i in tags:
    string_with_tag = field[i:]
    
    
    end =  get_word_end(string_with_tag)
    string_with_tag = string_with_tag[:end]
    
    if string_with_tag not in dictionary:
      dictionary[string_with_tag] = 1
    elif string_with_tag in dictionary:
      dictionary[string_with_tag] += 1
      
      
'''
Gets the index of the end of the word in a desired string
'''
def get_word_end(string):
  string = string[1:]
  for i in string:
     if i.isalpha() == False:
       return string.index(i) +1
  return -1

def detect_field_lang(field):
  global langs
  field_lang = detect(field)
  
  if field_lang not in langs:
    langs[field_lang] = 1
  elif field_lang in langs:
    langs[field_lang] += 1


'''--------------------------Interaction Analytics--------------------------'''
def find_most_retweets(lis, num):
  most_retweets = []
  for i in range(num):
    top = max(lis)
    tweet_line = list.index(top)
    
    

def find_retweets(field):
  
  temp = field
  i = 0
  while i < 4:
    
    index = temp.find(';')
    temp = temp[index+1:]
    
    i += 1
  
  index = temp.find(';')
  temp = temp[:index]
  
  return temp


def find_favorites(field):
  temp = field
  i = 0
  while i < 5:
    
    index = temp.find(';')
    temp = temp[index+1:]
    
    i += 1
  
  index = temp.find(',')
  temp = temp[:index]
  return temp

'''-----------------------Natural Language Processing-----------------------'''

def find_bigrams(tokens, num):
  bgm = nltk.collocations.BigramAssocMeasures()
  finder = BigramCollocationFinder.from_words(tokens)
  scored = finder.score_ngrams(bgm.likelihood_ratio)
  
  return scored[:num]
  

def find_trigrams(tokens, num):
  tgm = nltk.collocations.TrigramAssocMeasures()
  finder = TrigramCollocationFinder.from_words(tokens)
  scored = finder.score_ngrams(tgm.likelihood_ratio)
  
  return scored[:num]
  


'''-----------------------------Writing to file-----------------------------'''


file = input('Enter the csv file: ' )
num = int(input('Enter number of analytics fields to show ' ))

hashtags = {}
mentions = {'total mentions': 0, 'tweets with mentions': 0, 'tweets without mentions': 0}
favorites = []
retweets = []

tokens = tokenize_csv(file)


analytics_file_name = 'analytics_for_' + str(file[:-4]) + '.csv'

common_hashtags = (get_top_hashtags(hashtags, num))

mentions_per_data = ['Mentions per tweet', None]

mentions_ratio_data = [ 'Tweets with mentions: Tweets without', None]

mentions_per_tweet = get_mentions_per_tweet(mentions)
mentions_per_data[1] = mentions_per_tweet

mentions_ratio = get_mentions_ratio(mentions)
mentions_ratio_data[1] = mentions_ratio

bigrams = find_bigrams(tokens, num)
trigrams = find_trigrams(tokens, num)


with open(analytics_file_name, 'w') as csvfile:
  csv_writer = csv.writer(csvfile)
  
  csv_writer.writerow(['TWEET TEXT ANALYTICS'])
  
  csv_writer.writerow(['Commmon Hashtags'])
  csv_writer.writerow(common_hashtags)
  csv_writer.writerow('')
  
  csv_writer.writerow(['Mentions Analytics'])
  csv_writer.writerow(mentions_per_data)
  csv_writer.writerow(mentions_ratio_data)
  csv_writer.writerow('')
  
  csv_writer.writerow(['Common Two Word Phrases'])
  csv_writer.writerow(['Phrase', 'Likelihood Ratio'])
  csv_writer.writerows(bigrams)
  csv_writer.writerow('')
  
  csv_writer.writerow(['Common Three Word Phrases'])
  csv_writer.writerow(['Phrase', 'Likelihood Ratio'])
  csv_writer.writerows(trigrams)
