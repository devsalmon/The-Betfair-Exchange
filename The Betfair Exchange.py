#The Betfair Exchange
import requests
import json
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
APP_KEY = 'iym7OLs6r9EYcFYv'
SESSION_TOKEN = 'iCauS/9fh/fSS32gro11CbPcbd8e9RAYFedsMU9e8F4='
START_DATE = "2021-05-27T00:00:00Z"
END_DATE = "2021-05-27T23:59:00Z"

header = { 'X-Application' : APP_KEY, 'X-Authentication' : SESSION_TOKEN,'content-type' : 'application/json' }
 
## eventTypeIds is the id of event type.
json_req_football_events='{"filter":{ "eventTypeIds": ["1"], "marketStartTime": {"from": "2021-05-29T00:00:00Z", "to": "2021-05-29T23:59:00Z"} }}'

##                  LIST EVENTS
##[
##    {
##        "jsonrpc": "2.0",
##        "method": "SportsAPING/v1.0/listEvents",
##        "params": {
##            "filter": {
##                "eventTypeIds": [
##                    "1"
##                ],
##                "marketStartTime": {
##                    "from": "2014-03-13T00:00:00Z",
##                    "to": "2014-03-13T23:59:00Z"
##                }
##            }
##        },
##        "id": 1
##    }
##]

## eventIDs is the id of the match
json_req_football_match='{"filter":{ "eventIds": ["30494247"] }, "maxResults": "200", "marketProjection": ["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "RUNNER_DESCRIPTION", "RUNNER_METADATA", "MARKET_START_TIME"]}'

##                  LIST EVENT INFO
##[
##    {
##        "jsonrpc": "2.0",
##        "method": "SportsAPING/v1.0/listMarketCatalogue",
##        "params": {
##            "filter": {
##                "eventIds": [
##                    "27165685"
##                ]
##            },
##            "maxResults": "200",
##            "marketProjection": [
##                "COMPETITION",
##                "EVENT",
##                "EVENT_TYPE",
##                "RUNNER_DESCRIPTION",
##                "RUNNER_METADATA",
##                "MARKET_START_TIME"
##            ]
##        },
##        "id": 1
##    }
##]

## market id is id of market for that match
json_req_market_odds='{"marketIds": ["1.183050605"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true" }}'

##[{
##    "jsonrpc": "2.0",
##    "method": "SportsAPING/v1.0/listMarketBook",
##    "params": {
##        "marketIds": ["1.127771425"],
##        "priceProjection": {
##            "priceData": ["EX_BEST_OFFERS", "EX_TRADED"],
##            "virtualise": "true"
##        }
##    },
##    "id": 1
##}]
 
football_events_url = endpoint + "listEvents/"
football_match_url = endpoint + "listMarketCatalogue/"
match_market_url = endpoint + "listMarketBook/"
#test
 
football_events_response = requests.post(football_events_url, data=json_req_football_events, headers=header)
football_match_response = requests.post(football_match_url, data=json_req_football_match, headers=header)
match_market_response = requests.post(match_market_url, data=json_req_market_odds, headers=header)

## Prints list of football events
##print(json.dumps(json.loads(football_events_response.text), indent=3))
## Prints football match info
##print(json.dumps(json.loads(football_match_response.text), indent=3))
## Prints odds for market
##print(json.dumps(json.loads(match_market_response.text), indent=3))
y = json.loads(match_market_response.text)
print(y[0]['status'])
