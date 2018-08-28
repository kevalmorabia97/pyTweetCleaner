# pyTweetCleaner
Python module to clean twitter json data and remove unnecessary tweet data

**Usage1:**
```python
>>> from pyTweetCleaner import TweetCleaner
>>> tc = TweetCleaner(remove_stop_words=True, remove_retweets=True)
>>> tc.clean_tweets(input_file='data/sample_input.json', output_file='data/sample_output.json')
```

**Usage2:**
```python
>>> from pyTweetCleaner import TweetCleaner
>>> sample_text = 'RT @testUser: Cleaning unnecessary data with pyTweetCleaner by @kevalMorabia97. #pyTWEETCleaner, Check it out at https:\/\/github.com\/kevalmorabia97\/pyTweetCleaner and star the repo! '
>>>
>>> tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)
>>> print(tc.get_cleaned_text(sample_text))
RT @testUser: Cleaning unnecessary data pyTweetCleaner @kevalMorabia97 #pyTWEETCleaner Check star repo
>>>
>>> tc = TweetCleaner(remove_stop_words=False, remove_retweets=True)
>>> print(tc.get_cleaned_text(sample_text))
 
>>>
>>> tc = TweetCleaner(remove_stop_words=False, remove_retweets=False)
>>> print(tc.get_cleaned_text(sample_text))
RT @testUser: Cleaning unnecessary data with pyTweetCleaner by @kevalMorabia97 #pyTWEETCleaner Check it out at and star the repo

```


<hr>

**Requirements:**
1. nltk>=3.2.4
```
pip install -r requirements.txt
```

<hr>

**Data Removed and Kept:**
```
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
               geo
               coordinates
               place
               retweet_count
               entities
               retweeted_status
```

**Note:** If you want only some of these data fields then comment others in _pyTweetCleaner.py_ file.
<br>If you want other fields also then add them in _pyTweetCleaner.py_ 
