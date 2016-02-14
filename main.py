import random

import nltk
from nltk.corpus import wordnet as wn
import twitter
import keys
import io
import make_defintion_image
import bisect
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--dry_run", dest="dry_run", action="store_true")
(options, args) = parser.parse_args()

print 'Loading words ...'
#nouns, verbs, adjectives, adverbs = [list(wn.all_synsets(pos=POS)) for POS in [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]]
nouns = list(wn.all_synsets(pos=wn.NOUN))
print 'Done loading words ...'

def gen_phrase(*pattern): return [random.choice(i) for i in pattern]

def phrase_to_string(phrase): return ' '.join(s.lemmas[0].name for s in phrase)

def phrase_to_string(phrase): return ' '.join(s.lemmas[0].name for s in phrase)

def gen_password(): return phrase_to_string(gen_phrase(adverbs, adjectives, adjectives, nouns))

bird_patterns = [
  ('%sbird', 10),
  ('%s Eagle', 3),
  ('%s Owl', 3)
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

def get_weighted_entry(items):
  mysum = 0
  breakpoints = [] 
  items = list(items)

  for i in items:
    mysum += i['weight']
    breakpoints.append(mysum)
 
  print 'total: %s' % mysum
  score = random.randint(0, mysum - 1)
  print 'picking elem %s' % score
  
  runningsum = 0
  for i in items:
    if score >= runningsum and score < runningsum + i['weight']:
      return i
    runningsum += i['weight']

  return items[-1]


def get_weighted_item(items):
  mysum = 0
  breakpoints = [] 

  for i in items:
    mysum += i[1]
    breakpoints.append(mysum)
 
  print 'total: %s' % mysum
  score = random.randint(0, mysum - 1)
  print 'picking elem %s' % score
  
  runningsum = 0
  for i in items:
    if score >= runningsum and score < runningsum + i[1]:
      return i[0]
    runningsum += i[1]
  return items[-1]
  
def get_pattern():
  return get_weighted_item(bird_patterns)

def get_wordset():
  return get_weighted_entry(sets)

def make_name(noun):
  pattern = get_pattern()

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

def maybe_truncate(string, max_length=120):
  if len(string) > max_length:
    print 'too long, truncating'
    ret = string[:max_length-1] + u"\u2026"
    print ret
    print len(ret)
    return ret
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

  if not options.dry_run:
    print 'Posting to twitter ...'
    post_to_twitter(tweet, img_bytes)

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
    img_resp = t_up.media.upload(media=img_bytes)
    id_img1 = img_resp["media_id_string"]
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
