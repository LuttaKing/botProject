import json,requests
import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler
import random


sched = BlockingScheduler()

# Authenticate to Twitter
auth = tweepy.OAuthHandler('GDkH7vUmKyIi2lCMx4EsKK5TD','C5jCCw9kp7dp0wWdQt220M5u7yEX2M0AKy5vctd8rVvqTKdO5o')
auth.set_access_token("1033806755455807488-fJBc6jVnVvfVUNU6VTuRWxSzDRkTho","b9txmEiiZNJGUymtLFu0J6JSC8BQn7764NFvYWv1ToSPk")

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

reply_List=[
  'Interesting opinion right there,but what do I Know',
  'well,am going to like and reply to this since you clearly have no friends to do that for you',
  'am not really sure about this,please stop mentioning me on some bs,i will still like your post though',
  'your life is so sad,just like mine,i will still like your post though',
  'checked your account,you are shady,stop tagging me,i will still like your post though',
  'yeessir !!',

]
def check_mentions():
    twet_list=[]
    print("========================Retrieving mentions=====================================")
    rs=requests.get('https://birdie69.herokuapp.com/api/update_id')
    last_id=int(rs.text)
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=last_id).items():
           
            try:
              api.create_favorite(tweet.id)
            except Exception as e:
              print('Like Error: ' + str(e))
            
            try:
              random_reply=random.choice(reply_List)
            #  print(tweet.)
              api.update_status(
                status=random_reply,
                in_reply_to_status_id=tweet.id,
                 auto_populate_reply_metadata=True
              )
            except Exception as e:
              print('Reply Error: ' + str(e))
            
            twet_list.append(tweet)
    print('You have '+str(len(twet_list))+' new mentions')
    try:
      new_last_id=str(twet_list[-1].id)
      requests.post('https://birdie69.herokuapp.com/api/update_id',data={'old_tweetID':str(last_id),
      'new_tweetID':new_last_id})
    except Exception as e:
      print('No New Mentions Son so no new tweet ID posted')
    
    


check_mentions()
@sched.scheduled_job('interval', minutes=2)
def timed_job():
    check_mentions()

sched.start()