import twitter
import sys
import time
import json
from collections import Counter
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

# State definitions
AL = {"keys": [' AL', "BAMA"], "exceptions": ["ALB"], "name": "alabama", "accounts": []}
AK = {"keys": [' AK', "ALASKA"], "exceptions": [], "name": "alaska", "accounts": []}
AZ = {"keys": [' AZ', "ZONA"], "exceptions": ["AZE"], "name": "arizona", "accounts": []}
AR = {"keys": [' AR', "ARKANSAS"], "exceptions": ["ARE","ARG", "ARA", "ARD"], "name": "arkansas", "accounts": []}
CA = {"keys": [' CA', "CAL"], "exceptions": ["CANADA", "LOCAL", "CAR", "CAN", "CALC", "CAP", "CALA", "COLOMBIA", "CAM", "CAT"], "name": "california", "accounts": []}
CO = {"keys": [' CO', "COLORADO"], "exceptions": ["COUNTY", "CON", "COO", "COLU", "COLOM", "COA", "COM"], "name": "colorado", "accounts": []}
CT = {"keys": [' CT', "CONNECTICUT"], "exceptions": [], "name": "connecticut", "accounts": []}
DE = {"keys": [' DE', "DELAWARE"], "exceptions": ["DELH", " DE ", " DEL "], "name": "deleware", "accounts": []}
FL = {"keys": [' FL', "FLORIDA"], "exceptions": [], "name": "florida", "accounts": []}
GA = {"keys": [' GA', "GEORGIA", "ATL"], "exceptions": ["GAM", "GAN"], "name": "georgia", "accounts": []}
HI = {"keys": [' HI', "HAWAII"], "exceptions": ["HIGH", "HIM"], "name": "hawaii", "accounts": []}
ID = {"keys": [' ID', "IDAHO"], "exceptions": ["IDE"], "name": "idaho", "accounts": []}
IL = {"keys": [' IL', "ILLINOIS"], "exceptions": ["ILE"], "name": "illinois", "accounts": []}
IN = {"keys": [' IN', "INDIANA"], "exceptions": [" IN ", "INF", "INS", "INDO"], "name": "indiana", "accounts": []}
IA = {"keys": [' IA', "IOWA", "DES MOINES"], "exceptions": [], "name": "iowa", "accounts": []}
KS = {"keys": [' KS', "KANSAS"], "exceptions": [], "name": "kansas", "accounts": []}
KY = {"keys": [' KY', "KENTUCKY"], "exceptions": [], "name": "kentucky", "accounts": []}
LA = {"keys": [' LA', "LOUISIANA"], "exceptions": ["LAW", "LAB", "LAT", "LAN", "LAG", "LAK"], "name": "louisiana", "accounts": []}
ME = {"keys": [' ME', "MAINE"], "exceptions": ["MEX", " ME ", "MED"], "name": "maine", "accounts": []}
MD = {"keys": [' MD', "MARYLAND"], "exceptions": [], "name": "maryland", "accounts": []}
MA = {"keys": [' MA', "MASS"], "exceptions": ["LANDMASS", "MAT", "MAR", "MAI", "MAN", "MAL", "MAP"], "name": "massachusetts", "accounts": []}
MI = {"keys": [' MI', "MICHIGAN"], "exceptions": ["MIL", "MIN", "MIZ", "MIS", "MIR"], "name": "michigan", "accounts": []}
MN = {"keys": [' MN', "MINN"], "exceptions": [], "name": "minnesota", "accounts": []}
MS = {"keys": [' MS', "MISSISSIPPI"], "exceptions": [], "name": "mississippi", "accounts": []}
MO = {"keys": [' MO', "MISSOURI"], "exceptions": ["MOM", "MOO", "MON", "MOS", "MOI", "MOU"], "name": "missouri", "accounts": []}
MT = {"keys": [' MT', "MONTANA"], "exceptions": [], "name": "montana", "accounts": []}
NE = {"keys": [' NE', "NEBRASKA"], "exceptions": ["NEW", "NEU", "NEA", "NET"], "name": "nebraska", "accounts": []}
NV = {"keys": [' NV', "NEVADA"], "exceptions": [], "name": "nevada", "accounts": []}
NH = {"keys": [' NH', "NEW HAMPSHIRE"], "exceptions": [], "name": "new_hampshire", "accounts": []}
NJ = {"keys": [' NJ', "NEW JERSEY"], "exceptions": [], "name": "new_jersey", "accounts": []}
NM = {"keys": [' NM', "NEW MEXICO"], "exceptions": [], "name": "new_mexico", "accounts": []}
NY = {"keys": [' NY', "NEW YORK", "NYC", "N.Y.C"], "exceptions": [], "name": "new_york", "accounts": []}
NC = {"keys": [' NC', "NORTH CAROLINA"], "exceptions": [], "name": "north_carolina", "accounts": []}
ND = {"keys": [' ND', "NORTH DAKOTA"], "exceptions": [], "name": "north_dakota", "accounts": []}
OH = {"keys": [' OH', "OHIO"], "exceptions": [], "name": "ohio", "accounts": []}
OK = {"keys": [' OK', "OKLAHOMA"], "exceptions": [], "name": "oklahoma", "accounts": []}
OR = {"keys": [' OR', "OREGON"], "exceptions": ["ORI", " OR ", "ORD"], "name": "oregon", "accounts": []}
PA = {"keys": [' PA', "PENN", "PHILLY"], "exceptions": ["PAR", "PAK", "PAU", "PAN", "PAH"], "name": "pennsylvania", "accounts": []}
RI = {"keys": [' RI', "RHODE ISLAND"], "exceptions": ["RIC", "RIN"], "name": "rhode_island", "accounts": []}
SC = {"keys": [' SC', "SOUTH CAROLINA"], "exceptions": ["SCO"], "name": "south_carolina", "accounts": []}
SD = {"keys": [' SD', "SOUTH DAKOTA"], "exceptions": [], "name": "south_dakota", "accounts": []}
TN = {"keys": [' TN', "TENN"], "exceptions": [], "name": "tennessee", "accounts": []}
TX = {"keys": ['TX', "TEX"], "exceptions": [], "name": "texas", "accounts": []}
UT = {"keys": [' UT', "UTAH"], "exceptions": [], "name": "utah", "accounts": []}
VT = {"keys": [' VT', "VERMONT"], "exceptions": [], "name": "vermont", "accounts": []}
VA = {"keys": [' VA', "VIRGINIA"], "exceptions": ["VAN"], "name": "virginia", "accounts": []}
WA = {"keys": [' WA', "WASHINGTON"], "exceptions": ["WAF", "WAN", "WAL", "DC", "D.C"], "name": "washington", "accounts": []}
WV = {"keys": [' WV', "WEST VIRGINIA"], "exceptions": [], "name": "west_virginia", "accounts": []}
WI = {"keys": [' WI', "WISCONSIN"], "exceptions": [], "name": "wisconsin", "accounts": []}
WY = {"keys": [' WY', "WYOMING"], "exceptions": [], "name": "wyoming", "accounts": []}

# All 50 states
UNITED_STATES = [AL, AK, AZ, AR, CA, CO, CT, DE, FL, GA,
                 HI, ID, IL, IN, IA, KS, KY, LA, ME, MD,
                 MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ,
                 NM, NY, NC, ND, OH, OK, OR, PA, RI, SC,
                 SD, TN, TX, UT, VT, VA, WA, WV, WI, WY]

# Country definitions
INDIA = {"keys": ["INDIA", "MIZORAM", "DELH", "JAMMU"], "exceptions": ["INDIAN"], "name": "india", "accounts": []}
NIGERIA = {"keys": ["NIGERIA", "NIG"], "exceptions": [], "name": "nigeria", "accounts": []}
EGYPT = {"keys": ["EGYPT"], "exceptions": [], "name": "egypt", "accounts": []}
ENGLAND = {"keys": ["ENGLAND", "LONDON"], "exceptions": [], "name": "england", "accounts":[]}
GAMBIA = {"keys": ["GAMBIA"], "exceptions": [], "name": "gambia", "accounts": []}
ITALY = {"keys": ["ITALY", "ROME"], "exceptions": [], "name": "italy", "accounts": []}
JAPAN = {"keys": ["JAPAN", "TOKYO"], "exceptions": [], "name": "japan", "accounts": []}
CHILE = {"keys": ["CHILE"], "exceptions": [], "name": "chile", "accounts": []}
ALGERIA = {"keys": ["ALGERIA", "ALGERIE"], "exceptions": [], "name": "algeria", "accounts": []}
IVORY_COAST = {"keys": ["IVORY COAST"], "exceptions": [], "name": "ivory_coast", "accounts": []}
GERMANY = {"keys": ["GERMANY", "DEUTSCHLAND"], "exceptions": [], "name": "germany", "accounts": []}
SPAIN = {"keys": ["SPAIN"], "exceptions": [], "name": "spain", "accounts": []}
PORTUGAL = {"keys": ["PORTUGAL"], "exceptions": [], "name": "portugal", "accounts": []}
AUSTRALIA = {"keys": ["AUSTRALIA"], "exceptions": [], "name": "australia", "accounts": []}
FRANCE = {"keys": ["FRANCE", "ILE-DE-FRAN"], "exceptions": [], "name": "france", "accounts": []}
INDONESIA = {"keys": ["INDONESIA"], "exceptions": [], "name": "indonesia", "accounts": []}
MALAYSIA = {"keys": ["MALAYSIA", "KUALA", "PAHANG"], "exceptions": [], "name": "malaysia", "accounts": []}
PHILIPPINES = {"keys": ["TAGUIG", "PHILIPPINES"], "exceptions": [], "name": "philippines", "accounts": []}
COLOMBIA = {"keys": ["COLOMBIA"], "exceptions": [], "name": "colombia", "accounts": []}
SCOTLAND = {"keys": ["SCOTLAND"], "exceptions": [], "name": "scotland", "accounts": []}
BRAZIL = {"keys": ["BRAZIL", "BRA"], "exceptions": ["BRAU", "BRAI"], "name": "brazil", "accounts": []}
PAKISTAN = {"keys": ["PAKISTAN"], "exceptions": [], "name": "pakistan", "accounts": []}
NETHERLANDS = {"keys": ["NETHERLANDS"], "exceptions": [], "name": "netherlands", "accounts": []}
VENEZUELA = {"keys": ["VENEZUELA"], "exceptions": [], "name": "venezuela", "accounts": []}
CANADA = {"keys": ["CANADA", "ONTARIA", "BRITISH COLUMBIA", "ALBERTA", "VANCOUVER", "MANITOBA"], "exceptions": [], "name": "canada", "accounts": []}
SRI_LANKA = {"keys": ["SRI LANKA"], "exceptions": [], "name": "sri_lanka", "accounts": []}
ARGENTINA = {"keys": ["ARGENTINA"], "exceptions": [], "name": "argentina", "accounts": []}
IRAQ = {"keys": ["IRAQ"], "exceptions": [], "name": "iraq", "accounts": []}
UAE = {"keys": ["UNITED ARAB EMIRATES", "UAE", "DUBAI", "U.A.E"], "exceptions": [], "name": "united_arab_emirates", "accounts": []}
TURKEY = {"keys": ["TURKEY"], "exceptions": [], "name": "turkey", "accounts": []}
SAUDI_ARABIA = {"keys": ["SAUDI"], "exceptions": [], "name": "saudi_arabia", "accounts": []}
MEXICO = {"keys": ["MEXICO"], "exceptions": [], "name": "mexico", "accounts": []}
THAILAND = {"keys": ["THAILAND"], "exceptions": [], "name": "thailand", "accounts": []}
SOUTH_KOREA = {"keys": ["KOREA"], "exceptions": [], "name": "south_korea", "accounts": []}
IRELAND = {"keys": ["IRELAND"], "exceptions": [], "name": "ireland", "accounts": []}
WALES = {"keys": ["WALES"], "exceptions": [], "name": "wales", "accounts": []}
SWEDEN = {"keys": ["SWEDEN"], "exceptions": [], "name": "sweden", "accounts": []}
PUERTO_RICO = {"keys": ["PUERTO RICO"], "exceptions": [], "name": "puerto_rico", "accounts": []}
RUSSIA = {"keys": ["RUSSIA"], "exceptions": [], "name": "russia", "accounts": []}
BANGLADESH = {"keys": ["BANGLADESH"], "exceptions": [], "name": "bangladesh", "accounts": []}
ETHIOPIA = {"keys": ["ETHIOPIA"], "exceptions": [], "name": "ethiopia", "accounts": []}
VIETNAM = {"keys": ["VIETNAM"], "exceptions": [], "name": "vietnam", "accounts": []}
SOUTH_AFRICA = {"keys": ["SOUTH AFRICA"], "exceptions": [], "name": "south_africa", "accounts": []}
KENYA = {"keys": ["KENYA"], "exceptions": [], "name": "kenya", "accounts": []}
TANZANIA = {"keys": ["TANZANIA"], "exceptions": [], "name": "tanzania", "accounts": []}
MYANMAR = {"keys": ["MYANMAR"], "exceptions": [], "name": "myanmar", "accounts": []}
THAILAND = {"keys": ["THAILAND"], "exceptions": [], "name": "thailand", "accounts": []}
UGANDA = {"keys": ["UGANDA"], "exceptions": [], "name": "uganda", "accounts": []}
SUDAN = {"keys": ["SUDAN"], "exceptions": [], "name": "sudan", "accounts": []}
UKRAINE = {"keys": ["UKRAINE"], "exceptions": [], "name": "ukraine", "accounts": []}

# Countries with most twitter users
# Found at: https://www.statista.com/statistics/242606/number-of-active-twitter-users-in-selected-countries/
# Additional countries according to our data and total population
WORLD = [INDIA, NIGERIA, EGYPT, ENGLAND, GAMBIA, ITALY, JAPAN, CHILE, ALGERIA, IVORY_COAST, GERMANY, SPAIN,
         PORTUGAL, AUSTRALIA, FRANCE, INDONESIA, MALAYSIA, PHILIPPINES, COLOMBIA, SCOTLAND, BRAZIL, PAKISTAN,
         NETHERLANDS, VENEZUELA, CANADA, SRI_LANKA, ARGENTINA, IRAQ, UAE, TURKEY, SAUDI_ARABIA, MEXICO,
         THAILAND, SOUTH_KOREA, IRELAND, WALES, SWEDEN, PUERTO_RICO, RUSSIA, BANGLADESH, ETHIOPIA, VIETNAM,
         SOUTH_AFRICA, KENYA, TANZANIA, MYANMAR, THAILAND, UGANDA, SUDAN, UKRAINE]

# Converts json files to a list
def json_to_list(files=[]):
    accounts = []
    for f in files:
        with open(f) as data_file:    
            data = json.load(data_file)
            for item in data:
                accounts.append(item)
    return accounts

# Return and sort accounts with fetchable location, modified from TwitterCookbook.py
def get_user_location(twitter_api, user_ids, location_definitions):
    
    # Combines all location definitions
    for i in range(1, len(location_definitions)):
        location_definitions[0] += location_definitions[i]
    all_defs = location_definitions[0]

    items = user_ids

    # Iterate through all users
    while len(items) > 0:
        
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]
        # Fetch user info
        response = make_twitter_request(twitter_api.users.lookup, user_id=items_str)
        for user_info in response:
            # Sort by location
            location = user_info["location"].upper()
            if location != "":
                for definition in all_defs:
                    if any(key in location for key in definition["keys"]) and not any(exception in location for exception in definition["exceptions"]):
                        print("Location: " + user_info["location"] + "\n" + "Classifier: " + str(definition["keys"]) + "\n")
                        definition["accounts"].append(user_info["id"])
                        user_ids.remove(str(user_info["id"]))
                        break
            else:
                user_ids.remove(str(user_info["id"]))
                
    # Writes unsorted accounts to a file
    not_sorted = open("not_sorted.txt", "w")
    for uid in user_ids:
        not_sorted.write(uid)
    not_sorted.close


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


# Converts sports fan json files to list
accounts = json_to_list(["sportsFans1.json", "sportsFans2.json"])

# Gets location of all sports fans
get_user_location(twitter_api, accounts, [WORLD, UNITED_STATES])

print("DONE FETCHING LOCATIONS\n")

# Combines country and state definitions
definitions = WORLD + UNITED_STATES

# Iterate through location definitions
for location in definitions:
    all_friends = []
    accounts = location["accounts"]
    filename = location["name"]
    # Writes all local acocunts to file
    file = open("location_accounts/%s.txt" %filename, "w")
    for account in accounts:
        file.write(str(account)+"\n")
    
