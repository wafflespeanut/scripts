
import json
import os
import sys

from TwitterAPI import TwitterAPI
from time import sleep


DB_PATH = os.environ.get('DB_PATH', 'liked-tweets.dat')
REQ_PATH = 'favorites/list'
TWEETS_PER_BATCH = 200
SLEEP_SECS = (15 * 60) / 75     # 75 requests in 15-min window.

def collectFromStart(api, fd, stopId=None):
    lastId = None
    count = 0
    while True:
        params = {'count': TWEETS_PER_BATCH}
        if lastId is not None:
            params['max_id'] = lastId
        resp = api.request(REQ_PATH, params=params)
        tweets = resp.json()

        # Eliminate first tweet if we already have it.
        if tweets and tweets[0]['id'] == lastId:
            tweets = tweets[1:]

        if not tweets:
            return count

        for tweet in tweets:
            if tweet['id'] == stopId:
                return count

            fd.write(json.dumps(tweet))
            fd.write('\n')
            lastId = tweet['id']
            count += 1

        print('Collected %d tweets.' % count)
        sleep(SLEEP_SECS)


api = TwitterAPI(consumer_key=os.environ['CONS_KEY'],
                 consumer_secret=os.environ['CONS_SECRET'],
                 access_token_key=os.environ['ACCESS_KEY'],
                 access_token_secret=os.environ['ACCESS_SECRET'],
                 auth_type='oAuth1')

if os.path.exists(DB_PATH):
    tmpPath = DB_PATH + '.tmp'
    collected = 0
    with open(DB_PATH, 'r') as oldFd, open(tmpPath, 'w') as newFd:
        line = oldFd.readline()
        tweet = json.loads(line)
        firstId = tweet['id']
        collected = collectFromStart(api, newFd, stopId=firstId)
        if collected > 0:
            print('Found new tweets. Replacing old archive.')
            for line in oldFd:
                newFd.write(line)

    if collected > 0:
        os.rename(tmpPath, DB_PATH)
    else:
        os.remove(tmpPath)
    sys.exit()


print('Building archive from scratch...')
with open(DB_PATH, 'w') as fd:
    collectFromStart(api, fd)
