import random

import nltk
from nltk.corpus import wordnet as wn
import twitter
import keys

nouns, verbs, adjectives, adverbs = [list(wn.all_synsets(pos=POS)) for POS in [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]]

def gen_phrase(*pattern): return [random.choice(i) for i in pattern]

def phrase_to_string(phrase): return ' '.join(s.lemmas[0].name for s in phrase)

def phrase_to_string(phrase): return ' '.join(s.lemmas[0].name for s in phrase)

def gen_password(): return phrase_to_string(gen_phrase(adverbs, adjectives, adjectives, nouns))

bird_patterns = [
  '%sbird',
  '%s Eagle',
  '%s Owl'
]

service_nouns = [
  'frontend',
  'distributed store',
  'lockservice',
  'thrift service',
  'scala service',
  'service service',
  'mapreduce job',
  'offline computation',
  'complicated pipeline',
  'mobile sdk'
]

service_verbs = [
  'making',
  'creating',
  'computing',
  'servicing',
  'finding',
  'serving',
  'storing',
  'coordinating',
  'distributing'
]

def make_name(noun):
  pattern = random.choice(bird_patterns)

  if ' ' in pattern:
    name = pattern % noun.lemmas()[0].name().replace('_', ' ')
    return name.title()
  else:
    name = pattern % noun.lemmas()[0].name().replace('_', '')
    return name

def get_article(word):
  if word[0] in ['a', 'e', 'i', 'o', 'u']:
    return 'an'
  return 'a'

def make_definition(noun):
  service_noun = random.choice(service_nouns)

  return '%(article)s %(service_noun)s for %(verb)s %(definition)s' % {
    'article': get_article(service_noun),
    'service_noun': service_noun,
    'definition': noun.definition(),
    'verb': random.choice(service_verbs)
  }

def make_tweet():
  noun = random.choice(nouns)
  tweet = '%s - %s' % (make_name(noun), make_definition(noun))
  print tweet
  return tweet

def post_to_twitter(text, img_bytes):
  t = twitter.Twitter(auth = twitter.OAuth(
     keys.twitter_access_token, keys.twitter_access_token_secret,
     keys.twitter_consumer_key, keys.twitter_consumer_secret
  ))

  t_up = twitter.Twitter(domain = 'upload.twitter.com', auth = twitter.OAuth(
     keys.twitter_access_token, keys.twitter_access_token_secret,
     keys.twitter_consumer_key, keys.twitter_consumer_secret
  ))

  if img_bytes:
    id_img1 = t_up.media.upload(media=img_bytes)["media_id_string"]
  else:
    id_img1 = None

  if img_bytes:
    response = t.statuses.update(status=text, media_ids=id_img1)
  else:
    response = t.statuses.update(status=text)

  print 'http://twitter.com/%s/status/%s' % (response['user']['screen_name'], response['id'])

if __name__ == "__main__":
  tweet = make_tweet()
  post_to_twitter(tweet, [])
