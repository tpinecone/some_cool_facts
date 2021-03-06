import requests
import nltk
import tweepy
import secrets
nltk.download('punkt')

def find_fact():
  random_id_response = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json')
  random_id = random_id_response.json()['query']['random'][0]['id']
  page_response = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids={}".format(random_id))
  extract = page_response.json()['query']['pages'][str(random_id)]['extract']

  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  sentences = tokenizer.tokenize(extract)
  for sentence in sentences:
    if len(sentence) <= 140:
      return sentence
  find_fact()

def tweet(message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message {}".format(message))
  api.update_status(status=message)

tweet(find_fact())
