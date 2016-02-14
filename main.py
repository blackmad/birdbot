import random

import nltk
from nltk.corpus import wordnet as wn
import twitter
import keys
import io
import make_defintion_image

print 'Loading words ...'
#nouns, verbs, adjectives, adverbs = [list(wn.all_synsets(pos=POS)) for POS in [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]]
nouns = list(wn.all_synsets(pos=wn.NOUN))
print 'Done loading words ...'

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
  'distributed cache',
  'lockservice',
  'thrift service',
  'thrift api',
  'scala service',
  'finagle service',
]

offline_nouns = [
  'scalding job',
  'mapreduce job',
  'offline computation',
  'pipeline',
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
  'distributing',
  'transpiling'
]

offline_verbs = [
  'computing',
  'clustering',
  'calculating',
  'learning'
]

mobile_nouns = [
  'Android fragment',
  'iOS framework',
  'mobile SDK',
  'client app'
]

mobile_verbs = [
  'showing',
  'storing',
  'displaying',
  'collecting'
]

sets = [
  { 'noun': service_nouns, 'verb': service_verbs, 'weight': 10 },
  { 'noun': offline_nouns, 'verb': offline_verbs, 'weight': 4 },
  { 'noun': mobile_nouns, 'verb': mobile_verbs, 'weight': 3 }
]

def get_wordset():
  return random.choice(sets)

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

def make_full_definition(definition):
  wordset = get_wordset()

  filldict = {}
  for (k, v) in wordset.iteritems():
    if k is not 'weight':
      filldict[k] = random.choice(v)

  filldict['article'] = get_article(filldict['noun'])
  filldict['definition'] = definition

  service_noun = random.choice(service_nouns)

  return '%(article)s %(noun)s for %(verb)s %(definition)s' % filldict

def maybe_truncate(string, max_length=140):
  if len(string) > max_length:
    print 'too long, truncating'
    return string[:max_length-1] + u"\u2026"
  return string

def make_tweet():
  noun = random.choice(nouns)
  
  word = make_name(noun)
  definition = make_full_definition(noun.definition())

  tweet = '%s - %s' % (word, definition)

  print 'Making image ...'
  img = make_defintion_image.make(word, definition)

  with io.BytesIO() as output:
    img.save(output, 'JPEG')
    img_bytes = output.getvalue()

  print tweet

  print 'Posting to twitter ...'
  post_to_twitter(maybe_truncate(tweet), img_bytes)

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
  tweet = make_tweet()
  tweet = make_tweet()
  tweet = make_tweet()

  # post_to_twitter(tweet, [])
