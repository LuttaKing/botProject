import json,requests
import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# Authenticate to Twitter
auth = tweepy.OAuthHandler('GDkH7vUmKyIi2lCMx4EsKK5TD','C5jCCw9kp7dp0wWdQt220M5u7yEX2M0AKy5vctd8rVvqTKdO5o')
auth.set_access_token("1033806755455807488-Jt8IXRMXFKa62Sr7PCR0Q3w44A75LA","otSHxAxgt04CwlGheftiuHiwFMgocqW0vIMID5iMkuNEP")

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

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
              api.update_status(
                status=" a bot script replied to this",
                in_reply_to_status_id=tweet.id,
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
    
    



# @sched.scheduled_job('interval', minutes=5)
# def timed_job():
#     check_mentions()

# sched.start()