import twitter
from collections import Counter
import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine

# API TOKENS AND KEYS
CONSUMER_KEY = 'WqDSnhSuwdMuySZgCmD2sydwZ'
CONSUMER_SECRET = 'vVAqj0rOFcEPunAvICKrgkVzu76KOAIZwzhApZKDiEybGO9Vuy'
OAUTH_TOKEN = '2992719835-B1yKnNmOPFzq47ZyzA9FlKLIO7G2RToOv8QA7l9'
OAUTH_TOKEN_SECRET = '8F5UDMYEXv5pxBqthnlSdYpjbg7IonRKmsYZoHuwPloIn'

#test
CONSUMER_KEY = 'e8zmBf7c6dCNSIYyOe3VOpAQi'
CONSUMER_SECRET = '5TQ7g42GbgQfEdjOVMSS17gewLp65mfN6GTXYcIOVSuL9BLRyl'
OAUTH_TOKEN = '2992719835-B1yKnNmOPFzq47ZyzA9FlKLIO7G2RToOv8QA7l9'
OAUTH_TOKEN_SECRET = '8F5UDMYEXv5pxBqthnlSdYpjbg7IonRKmsYZoHuwPloIn'

# AUTHORIZATION
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# File names for sports fans of each state
files = ["alaska.txt", "alabama.txt", "arkansas.txt", "arizona.txt", "california.txt", "colorado.txt",
         "connecticut.txt", "deleware.txt", "florida.txt", "georgia.txt", "hawaii.txt", "idaho.txt",
         "illinois.txt", "indiana.txt", "iowa.txt", "kansas.txt", "kentucky.txt", "louisiana.txt",
         "maine.txt", "maryland.txt", "massachusetts.txt", "michigan.txt", "minnesota.txt", "mississippi.txt",
         "missouri.txt", "montana.txt", "nebraska.txt", "nevada.txt", "new_hampshire.txt", "new_jersey.txt",
         "new_mexico.txt", "new_york.txt", "north_carolina.txt", "north_dakota.txt", "ohio.txt", "oklahoma.txt",
         "oregon.txt", "pennsylvania.txt", "rhode_island.txt", "south_carolina.txt", "south_dakota.txt",
         "south_dakota.txt", "tennessee.txt", "texas.txt", "utah.txt", "vermont.txt", "virginia.txt",
         "washington.txt", "wisconsin.txt", "wyoming.txt"]

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

# Writes the most popular accounts for each state to a file
for file in files:
    # Gets most popular accounts for each location
    most_pop = get_friends(twitter_api, "location_accounts/"+file)
    ranked = open("location_influencers/"+file, "w")
    # Writes accounts to file
    for item in most_pop:
        ranked.write(item)
    ranked.close
