import twitter
from collections import Counter
import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine

# API TOKENS AND KEYS
CONSUMER_KEY = 'yktLWxSyAD6iyX5IX1nEtuIzd'
CONSUMER_SECRET = 'wePrx9zAAM79abqhGdVm9eQmvBQyroBqmjF4VCIQ9KQnxQQwuk'
OAUTH_TOKEN = 'B1yKnNmOPFzq47ZyzA9FlKLIO7G2RToOv8QA7l9'
OAUTH_TOKEN_SECRET = '8F5UDMYEXv5pxBqthnlSdYpjbg7IonRKmsYZoHuwPloIn'

# AUTHORIZATION
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# File names for sports fans of each country
files = ["india.txt"," nigeria.txt," "egypt.txt", "england.txt", "gambia.txt", "italy.txt", "japan.txt", 
         "chile.txt", "algeria.txt", "ivory_coast.txt", "germany.txt", "spain.txt", "portugal.txt", 
         "australia.txt", "france.txt", "indonesia.txt", "malaysia.txt", "philippines.txt", 
         "colombia.txt", "scotland.txt", "brazil.txt", "pakistan.txt", "netherlands.txt",
         "venezuela.txt", "canada.txt", "sri_lanka.txt", "argentina.txt", "iraq.txt", "uae.txt", 
         "turkey.txt", "saudi_arabia.txt", "mexico.txt", "thailand.txt", "south_korea.txt",
         "ireland.txt", "wales.txt", "sweden.txt", "puerto_rico.txt", "russia.txt", "bangladesh.txt",
         "ethiopia.txt", "vietnam.txt", "south_africa.txt", "kenya.txt", "tanzania.txt", "myanmar.txt",
         "thailand.txt", "uganda.txt", "sudan.txt", "ukraine.txt"]

# Finds most followed friend among the friends list of 
def get_friends(twitter_api, file):
    accounts = open(file, "r")
    total_friends = []
    # Iterates through file
    for account in accounts:
        # Fetches friends for each user
        friends = make_twitter_request(twitter_api.friends.ids, user_id=account)
        # Adds all friends to list
        if friends != None:
            total_following += friends["ids"]
    # Sorts all friends by number of appearance
    influencers = Counter(total_following).most_common()
    accounts.close()
    # Returns influencer rank
    return influencers

# Error handling function from TwitterCookbook.py
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("SLEEPING... WILL RETRY IN 15 MINUTES", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print("BACK TO WORK", file=sys.stderr)
                print()
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'.format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

# Writes the most popular accounts for each country to a file
for file in files:
    # Gets most popular accounts for each location
    most_pop = get_friends(twitter_api, "location_accounts/"+file)
    ranked = open("location_influencers/"+file, "w")
    # Writes accounts to file
    for item in most_pop:
        ranked.write(item)
    ranked.close



