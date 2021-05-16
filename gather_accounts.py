import twitter
import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine

# API TOKENS AND KEYS
CONSUMER_KEY = 'e8zmBf7c6dCNSIYyOe3VOpAQi'
CONSUMER_SECRET = '5TQ7g42GbgQfEdjOVMSS17gewLp65mfN6GTXYcIOVSuL9BLRyl'
OAUTH_TOKEN = '2992719835-B1yKnNmOPFzq47ZyzA9FlKLIO7G2RToOv8QA7l9'
OAUTH_TOKEN_SECRET = '8F5UDMYEXv5pxBqthnlSdYpjbg7IonRKmsYZoHuwPloIn'

# AUTHORIZATION
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# Most popular sports twitter accounts (excluding individual teams and players)
# Found at: https://www.socialbakers.com/statistics/twitter/profiles/sport/page-1-4
# Minimum followers capped at 3 Million
sport_account_usernames = ["ChampionsLeague", "NBA", "NFL", "premierleague", "FIFAcom",
                           "BCCI", "ICC", "WWE", "MLB", "ufc", "EuropaLeague", "FIFAWorldCup",
                           "NHL", "IPL", "Olympics", "WWEUniverse", "LaLiga", "UEFAcom",
                           "fifacom_es", "fifacom_ar", "Wimbledon", "NASCAR", "MLS",
                           "LigaBBVAMX", "TheRealPCB"]

# Get a combined list of followers for multiple accounts
def get_followers_mult_accounts(twitter_api, accounts):
    data = open("sports_fans_ids.txt", "w")
    # Iterates through accounts
    for account in accounts:
        followers_gathered = 0
        more_followers = True
        # Gathers followers of an account
        followers = make_twitter_request(twitter_api.followers.ids, screen_name=account)
        # Gathers 250,000 followers for each account
        while followers_gathered < 250000:
            for fid in followers["ids"]:
                # Writes followers to file
                data.write(str(fid)+"\n")
                followers_gathered += 1
            if followers["next_cursor"] == 0:
                more_followers = False
            else: 
                followers = make_twitter_request(twitter_api.followers.ids, screen_name=account, cursor=followers["next_cursor"])
            print(followers_gathered)
    data.close()

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

# Executes function to gather sports fans
get_followers_mult_accounts(twitter_api, sport_account_usernames)
