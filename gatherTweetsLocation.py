# followed nltk tutorials found at: 
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
# https://stackabuse.com/sentiment-analysis-in-python-with-textblob/
import re, string
from textblob import TextBlob
import twitter
import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine

# CONSTANTS
NUM_TWEETS = 100

# API TOKENS AND KEYS
CONSUMER_KEY = 'e8zmBf7c6dCNSIYyOe3VOpAQi'
CONSUMER_SECRET = '5TQ7g42GbgQfEdjOVMSS17gewLp65mfN6GTXYcIOVSuL9BLRyl'
OAUTH_TOKEN = '2992719835-B1yKnNmOPFzq47ZyzA9FlKLIO7G2RToOv8QA7l9'
OAUTH_TOKEN_SECRET = '8F5UDMYEXv5pxBqthnlSdYpjbg7IonRKmsYZoHuwPloIn'

# AUTHORIZATION
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# STATE DATA
ALABAMA = {"bb": "33.518589,-86.810357,25mi", "name": "alabama", "data": []}
ALASKA = {"bb": "61.445587,-149.933304,25mi", "name": "alaska", "data": []}
ARIZONA = {"bb": "33.438078,-112.070892,25mi", "name": "arizona", "data": []}
ARKANSAS = {"bb": "34.736751,-92.277623,25mi", "name": "arkansas", "data": []}
CALIFORNIA = {"bb": "34.053691,-118.242766,25mi", "name": "california", "data": []}
COLORADO = {"bb": "39.739236,-104.984862,25mi", "name": "colorado", "data": []}
CONNECTICUT = {"bb": "41.489931,-73.241652,25mi", "name": "connecticut", "data": []}
DELAWARE = {"bb": "39.744655,-75.548391,25mi", "name": "delaware", "data": []}
FLORIDA = {"bb": "30.256303,-81.771027,25mi", "name": "florida", "data": []}
GEORGIA = {"bb": "33.748992,-84.390264,25mi", "name": "georgia", "data": []}
HAWAII = {"bb": "21.406846,-157.943567,25mi", "name": "hawaii", "data": []}
IDAHO = {"bb": "43.616616,-116.200886,25mi", "name": "idaho", "data": []}
ILLINOIS = {"bb": "41.8781,-87.6298,25mi", "name": "illinois", "data": []}
INDIANA = {"bb": "39.7684,-86.1581,25mi", "name": "indiana", "data": []}
IOWA = {"bb": "41.5868,-93.6250,25mi", "name": "iowa", "data": []}
KANSAS = {"bb": "37.692236,-97.337545,25mi", "name": "kansas", "data": []}
KENTUCKY = {"bb": "38.254238,-85.759407,25mi", "name": "kentucky", "data": []}
LOUISIANA = {"bb": "29.949932,-90.070116,25mi", "name": "louisiana", "data": []}
MAINE = {"bb": "43.827702,-70.348243,25mi", "name": "maine", "data": []}
MARYLAND = {"bb": "39.227082,-76.857951,25mi", "name": "maryland", "data": []}
MASSACHUSETTS = {"bb": "42.348075,-71.184634,25mi", "name": "massachusetts", "data": []}
MICHIGAN = {"bb": "42.355896,-83.134507,25mi", "name": "michigan", "data": []}
MINNESOTA = {"bb": "44.977300,-93.265469,25mi", "name": "minnesota", "data": []}
MISSISSIPPI = {"bb": "32.299038,-90.184769,25mi", "name": "mississippi", "data": []}
MISSOURI = {"bb": "39.100105,-94.578142,25mi", "name": "missouri", "data": []}
MONTANA = {"bb": "45.787496,-108.496070,25mi", "name": "montana", "data": []}
NEBRASKA = {"bb": "41.258746,-95.938376,25mi", "name": "nebraska", "data": []}
NEVADA = {"bb": "36.167256,-115.148516,25mi", "name": "nevada", "data": []}
NEW_HAMPSHIRE = {"bb": "42.995640,-71.454789", "name": "new_hampshire", "data": []}
NEW_JERSEY = {"bb": "40.681547,-74.392112,25mi", "name": "new_jersey", "data": []}
NEW_MEXICO = {"bb": "35.084103,-106.650985,25mi", "name": "new_mexico", "data": []}
NEW_YORK = {"bb": "40.712728,-74.006015,25mi", "name": "new_york", "data": []}
NORTH_CAROLINA = {"bb": "35.227209,-80.843083,25mi", "name": "north_carolina", "data": []}
NORTH_DAKOTA = {"bb": "46.877229,-96.789821,25mi", "name": "north_dakota", "data": []}
OHIO = {"bb": "39.962260,-83.000707,25mi", "name": "ohio", "data": []}
OKLAHOMA = {"bb": "35.472989,-97.517054,25mi", "name": "oklahoma", "data": []}
OREGON = {"bb": "45.520247,-122.674195,25mi", "name": "oregon", "data": []}
PENNSYLVANIA = {"bb": "39.952724,-75.163526,25mi", "name": "pennsylvania", "data": []}
RHODE_ISLAND = {"bb": "41.8240,-71.4128,25mi", "name": "rhode_island", "data": []}
SOUTH_CAROLINA = {"bb": "32.7765,-79.9311,25mi", "name": "south_carolina", "data": []}
SOUTH_DAKOTA = {"bb": "43.5460,-96.7313,25mi", "name": "south_dakota", "data": []}
TENNESSEE = {"bb": "36.1627,-86.7816,25mi", "name": "tennessee", "data": []}
TEXAS = {"bb": "29.7604,-95.3698,25mi", "name": "texas", "data": []}
UTAH = {"bb": "40.7608,-111.8910,25mi", "name": "utah", "data": []}
VERMONT = {"bb": "44.4759,-73.2121,25mi", "name": "vermont", "data": []}
VIRGINIA = {"bb": "36.8529,-75.9780,25mi", "name": "virginia", "data": []}
WASHINGTON = {"bb": "47.6062,-122.3321,25mi", "name": "washington", "data": []}
WEST_VIRGINIA = {"bb": "38.3498,-81.6326,25mi", "name": "west_virginia", "data": []}
WISCONSIN = {"bb": "43.0389,-87.9065,25mi", "name": "wisconsin", "data": []}
WYOMING = {"bb": "41.1400,-104.8202,25mi", "name": "wyoming", "data": []}

# All 50 States
states = [GEORGIA,ALABAMA, ALASKA, ARIZONA, ARKANSAS, CALIFORNIA, COLORADO, 
          CONNECTICUT, DELAWARE, FLORIDA, HAWAII, IDAHO, ILLINOIS,
          INDIANA, IOWA, KANSAS, KENTUCKY, LOUISIANA, MAINE, MARYLAND,
          MASSACHUSETTS, MICHIGAN, MINNESOTA, MISSISSIPPI, MISSOURI,
          MONTANA, NEBRASKA, NEVADA, NEW_HAMPSHIRE, NEW_JERSEY, NEW_MEXICO,
          NEW_YORK, NORTH_CAROLINA, NORTH_DAKOTA, OHIO, OKLAHOMA, OREGON,
          PENNSYLVANIA, RHODE_ISLAND, SOUTH_CAROLINA, SOUTH_DAKOTA, TENNESSEE,
          TEXAS, UTAH, VERMONT, VIRGINIA, WASHINGTON, WEST_VIRGINIA, WISCONSIN, WYOMING]

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

# Fetches at most 100 tweets given a search term and a geocode location
def get_tweets(twitter_api, query, location, num_tweets):
    num_gathered = 0
    # Fetches tweets
    response = make_twitter_request(twitter_api.search.tweets, q = query, geocode = location, count=num_tweets)
    # Returns list of tweets
    for tweet in response["statuses"]:
        if tweet["text"] not in tweets:
            tweets.append(tweet["text"])
            num_gathered += 1
    return tweets

# Analyzes tweet sentiment
def tweet_sentiment(tweet):
    text = TextBlob(tweet)
    # Returns polarity and subjectivity
    data = {"pol": text.polarity, "sub": text.subjectivity}
    return data

# Removes all hyperlinks, hashtags, and intrusive data
def clean_tweet(tweet):
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet) 
    return tweet

# Converts text file to a list
def txt_to_lst(file_name):
    lst = []
    file = open(file_name, "r")
    for line in file:
        lst.append(line[:-1])
    file.close
    return lst

# Creates list of league's team names
nba = {"teams": txt_to_lst("team_names/NBA.txt"), "name": "nba"}
nfl = {"teams": txt_to_lst("team_names/NFL.txt"), "name": "nfl"}
mlb = {"teams": txt_to_lst("team_names/MLB.txt"), "name": "mlb"}
nhl = {"teams": txt_to_lst("team_names/NHL.txt"), "name": "nhl"}

# Leagues to gather data for (FEEL FREE TO CHANGE)
leagues = [nba, nfl, mlb, nhl]

# MAIN FUNCTION
if __name__ == "__main__":
    for state in states:
        for league in leagues:
            # Creates a file corresponding to each league for each state
            file = open("location_team_rank/%s/%s.txt" %(league["name"], state["name"]), "w", encoding="utf-8")
            # Iterates through each team
            for team in league["teams"]:
                tweets = []
                avg_polarity = 0
                avg_subjectivity = 0
                # Gathers tweets about given team, in given location
                tweets = get_tweets(twitter_api, team, state["bb"], NUM_TWEETS)
                print("\n"+str(len(tweets))+" tweets gathered about "+team+" in "+state["name"]+"\n")
                # Iterates through tweets
                for tweet in tweets:
                    # Cleans and analyzes tweet
                    sentiment = tweet_sentiment(clean_tweet(tweet))
                    avg_polarity += sentiment["pol"]
                    avg_subjectivity += sentiment["sub"]
                if len(tweets) == 0:
                    divisor = 1
                else:
                    divisor = len(tweets)
                # Calculates average sentiment values
                avg_polarity = (avg_polarity/divisor)
                avg_subjectivity = (avg_subjectivity/divisor)
                team_data = {"name": team, "pol": avg_polarity, "sub": avg_subjectivity, "num_tweets": len(tweets)}
                state["data"].append(team_data)
            # Sorts each state's data
            sorted_data = sorted(state["data"], key = lambda i: i["pol"],reverse=True)
            # Writes sorted data to file
            for x in sorted_data:
                file.write(x["name"]+": "+str(x["num_tweets"]) +" tweets gathered\nPolarity: "+str(x["pol"])+"\tSubjectivity: "+str(x["sub"])+"\n\n")
            file.close()
