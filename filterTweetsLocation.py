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

# BOUNDING BOXES
ALABAMA = "[-88.473227 30.223334 -84.88908 35.008028]"
ALASKA = "[-179.148909 51.214183 179.77847 71.365162]"
ARIZONA = "[-114.81651 31.332177 -109.045223 37.00426]"
ARKANSAS = "[-94.617919 33.004106 -89.644395 36.4996]"
CALIFORNIA = "[-124.409591 32.534156 -114.131211 42.009518]"
COLORADO = "[-109.060253 36.992426 -102.041524 41.003444]"
CONNECTICUT = "[-73.727775 40.980144 -71.786994 42.050587]"
DELAWARE = "[-75.788658 38.451013 -75.048939 39.839007]"
FLORIDA = "[-87.634938 24.523096 -80.031362 31.000888]"
GEORGIA = "[-85.605165 30.357851 -80.839729 35.000659]"
HAWAII = "[-178.334698 18.910361 -154.806773 28.402123]"
IDAHO = "[-117.243027 41.988057 -111.043564 49.001146]"
ILLINOIS = "[-91.513079 36.970298 -87.494756 42.508481]"
INDIANA = "[-88.09776 37.771742 -84.784579 41.760592]"
IOWA = "[-96.639704 40.375501 -90.140061 43.501196]"
KANSAS = "[-102.051744 36.993016 -94.588413 40.003162]"
KENTUCKY = "[-89.571509 36.497129 -81.964971 39.147458]"
LOUISIANA = "[-94.043147 28.928609 -88.817017 33.019457]"
MAINE = "[-71.083924 42.977764 -66.949895 47.459686]"
MARYLAND = "[-79.487651 37.911717 -75.048939 39.723043]"
MASSACHUSETTS = "[-73.508142 41.237964 -69.928393 42.886589]"
MICHIGAN = "[-90.418136 41.696118 -82.413474 48.2388]"
MINNESOTA = "[-97.239209 43.499356 -89.491739 49.384358]"
MISSISSIPPI = "[-91.655009 30.173943 -88.097888 34.996052]"
MISSOURI = "[-95.774704 35.995683 -89.098843 40.61364]"
MONTANA = "[-116.050003	44.358221 -104.039138 49.00139]"
NEBRASKA = "[-104.053514 39.999998 -95.30829 43.001708]"
NEVADA = "[-120.005746 35.001857 -114.039648 42.002207]"
NEW_HAMPSHIRE = "[-72.557247 42.69699 -70.610621 45.305476]"
NEW_JERSEY = "[-75.559614 38.928519 -73.893979 41.357423]"
NEW_MEXICO = "[-109.050173 31.332301 -103.001964 37.000232]"
NEW_YORK = "[-79.762152 40.496103 -71.856214 45.01585]"
NORTH_CAROLINA = "[-84.321869 33.842316	-75.460621 36.588117]"
NORTH_DAKOTA = "[-104.0489 45.935054 -96.554507 49.00057]"
OHIO = "[-84.820159 38.403202 -80.518693 41.977523]"
OKLAHOMA = "[-103.002565 33.615833 -94.430662 37.002206]"
OREGON = "[-124.566244 41.991794 -116.463504 46.292035]"
PENNSYLVANIA = "[-80.519891 39.7198 -74.689516 42.26986]"
RHODE_ISLAND = "[-71.862772	41.146339 -71.12057	42.018798]"
SOUTH_CAROLINA = "[-83.35391 32.0346 -78.54203 35.215402]"
SOUTH_DAKOTA = "[-104.057698 42.479635 -96.436589 45.94545]"
TENNESSEE = "[-90.310298 34.982972 -81.6469 36.678118]"
TEXAS = "[-106.645646 25.837377 -93.508292 36.500704]"
UTAH = "[-114.052962 36.997968 -109.041058 42.001567]"
VERMONT = "[-73.43774 42.726853 -71.464555 45.016659]"
VIRGINIA = "[-83.675395	36.540738 -75.242266 39.466012]"
WASHINGTON = "[-124.763068 45.543541 -116.915989 49.002494]"
WEST_VIRGINIA = "[-82.644739 37.201483 -77.719519 40.638801]"
WISCONSIN = "[	-92.888114 42.491983 -86.805415 47.080621]"
WYOMING = "[-111.056888 40.994746 -104.05216 45.005904]"

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


tweets = make_twitter_request(twitter_api.search.tweets, q = "Golden State Warriors", count = 10, bounding_box = CALIFORNIA)

print(tweets)

for tweet in tweets["statuses"]:
    print(tweet["text"])
    print()
