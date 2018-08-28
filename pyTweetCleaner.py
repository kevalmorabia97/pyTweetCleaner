#!/usr/bin/env python

"""
pyTweetCleaner.py: Python module to clean twitter json data and remove unnecessary tweet data

REMOVE:        TWEETS THAT HAVE in_reply_to_status_id !=null i.e. COMMENTS ON SOMEONE ELSE'S TWEETS
               TWEETS THAT HAVE lang != en i.e. NOT IN ENGLISH LANGUAGE
               DATA ABOUT DELETED TWEETS
               NON-ASCII CHARACTERS FROM text
               HYPERLINKS FROM text
  
KEEP:          created_at
               id
               text
               user_id
               user_name
               user_screen_name
               user_followers_count
               coordinates
               place
               retweet_count
               entities
               retweeted_status
"""

__author__ = 'Keval Morabia'
__license__ = 'MIT'
__email__ = 'kevalmorabia97@gmail.com'

import json
import re
import string 

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TweetCleaner:
    def __init__(self, remove_stop_words=False, remove_retweets=False):
        """
        clean unnecessary twitter data
        remove_stop_words = True if stopwords are to be removed (default = False)
        remove_retweets = True if retweets are to be removed (default = False)
        """
        
        if remove_stop_words: self.stop_words = set(stopwords.words('english'))
        else: self.stop_words = set()
        
        self.remove_retweets = remove_retweets
        
        self.punc_table = str.maketrans("", "", string.punctuation) # to remove punctuation from each word in tokenize
    
    def compound_word_split(self, compound_word):
        """
        Split a given compound word(string) and return list of words in given compound_word
        Ex: compound_word='pyTWEETCleaner' --> ['py', 'TWEET', 'Cleaner']
        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', compound_word)
        return [m.group(0) for m in matches]
    
    def remove_non_ascii_chars(self, text):
        """
        return text after removing non-ascii characters i.e. characters with ascii value >= 128
        """
        return ''.join([w if ord(w) < 128 else ' ' for w in text])
    
    def remove_hyperlinks(self,text):
        """
        return text after removing hyperlinks
        """
        return ' '.join([w for w in text.split(' ')  if not 'http' in w])
      
    def get_cleaned_text(self, text):
        """
        return cleaned text(string) for provided tweet text(string)
        """
        cleaned_text = text.replace('\"','').replace('\'','').replace('-',' ')
            
        cleaned_text =  self.remove_non_ascii_chars(cleaned_text)
        
        # retweet
        if re.match(r'RT @[_A-Za-z0-9]+:',cleaned_text): # retweet
            if self.remove_retweets: return ''
            retweet_info = cleaned_text[:cleaned_text.index(':')+2] # 'RT @name: ' will be again added in the text after cleaning
            cleaned_text = cleaned_text[cleaned_text.index(':')+2:]
        else:
            retweet_info = ''
            
        cleaned_text = self.remove_hyperlinks(cleaned_text)
        
        cleaned_text = cleaned_text.replace('#','HASHTAGSYMBOL').replace('@','ATSYMBOL') # to avoid being removed while removing punctuations
        
        tokens = [w.translate(self.punc_table) for w in word_tokenize(cleaned_text)] # remove punctuations and tokenize
        tokens = [w for w in tokens if not w.lower() in self.stop_words and len(w)>1] # remove stopwords and single length words
        cleaned_text = ' '.join(tokens)
        
        cleaned_text = cleaned_text.replace('HASHTAGSYMBOL','#').replace('ATSYMBOL','@')
        cleaned_text = retweet_info + cleaned_text
        
        return cleaned_text
        
    def get_cleaned_tweet(self, tweet):
        """
        return a json dictionary of cleaned data from provided original tweet json dictionary
        """
        if not "created_at" in tweet: return None # remove info about deleted tweets
        if not tweet['lang'] == 'en': return None # remove tweets in non english language
        if not tweet['in_reply_to_status_id'] == None or not tweet['in_reply_to_user_id'] == None: return None # remove comments of any tweet
        
        cleaned_text = self.get_cleaned_text(tweet['text'])
        if cleaned_text == '': return None

        cleaned_tweet = {}
        
        cleaned_tweet['created_at'] = tweet['created_at']
        cleaned_tweet['id'] = tweet['id']
        cleaned_tweet['text'] = cleaned_text
        
        cleaned_tweet['user'] = {}
        cleaned_tweet['user']['id'] = tweet['user']['id']
        cleaned_tweet['user']['name'] = tweet['user']['name']
        cleaned_tweet['user']['screen_name'] = tweet['user']['screen_name']
        cleaned_tweet['user']['followers_count'] = tweet['user']['followers_count']
         
        cleaned_tweet['coordinates'] = tweet['coordinates']
        cleaned_tweet['place'] = tweet['place']
        cleaned_tweet['retweet_count'] = tweet['retweet_count']
        cleaned_tweet['entities'] = tweet['entities']

        return cleaned_tweet

    def clean_tweets(self, input_file, output_file='cleaned_tweets.json'):    
        """
        input_file: name or path of input twitter json data where each line is a json tweet
        output_file: file name or path where cleaned twitter json data is stored (default='cleaned_tweets.json')
        """
        in_file = open(input_file, 'r')
        out_file = open(output_file, 'w')
        
        while True:
            line = in_file.readline()
            if line=='': break
            tweet = json.loads(line)
            
            cleaned_tweet = self.get_cleaned_tweet(tweet)
            if cleaned_tweet == None: continue
            
            if 'retweeted_status' in tweet: # will be present if it is a retweet
                cleaned_tweet['retweeted_status'] = self.get_cleaned_tweet(tweet['retweeted_status'])
                if cleaned_tweet['retweeted_status'] == None: continue
                
            out_file.write(json.dumps(cleaned_tweet)+'\n')
        
        in_file.close()
        out_file.close()
    
if __name__  == '__main__':
    sample_text = 'RT @testUser: Cleaning unnecessary data with pyTweetCleaner by @kevalMorabia97. #pyTWEETCleaner, Check it out at https:\/\/github.com\/kevalmorabia97\/pyTweetCleaner and star the repo!'
     
    tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)
    tc.clean_tweets(input_file='data/sample_input.json', output_file='data/sample_output.json') # clean tweets from entire file
    print('Output with remove_stop_words=True, remove_retweets=False:')
    print(tc.get_cleaned_text(sample_text), '\n')
    
    tc = TweetCleaner(remove_stop_words=False, remove_retweets=True)
    print('Output with remove_stop_words=False, remove_retweets=True:')
    print(tc.get_cleaned_text(sample_text), '\n')
    
    tc = TweetCleaner(remove_stop_words=False, remove_retweets=False)
    print('Output with remove_stop_words=False, remove_retweets=False:')
    print(tc.get_cleaned_text(sample_text))
