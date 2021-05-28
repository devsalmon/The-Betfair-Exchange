#The Betfair Exchange
import requests
import json
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
APP_KEY = 'iym7OLs6r9EYcFYv'
SESSION_TOKEN = 'iCauS/9fh/fSS32gro11CbPcbd8e9RAYFedsMU9e8F4='
footballID = "1"
eventID = ''
marketID = ''
START_DATE = "2021-05-29T18:59:00Z"
END_DATE = "2021-05-29T19:59:00Z"
football_events_url = endpoint + "listEvents/"
football_match_url = endpoint + "listMarketCatalogue/"
match_market_url = endpoint + "listMarketBook/"

match_sought_for = input("Football Match: ")

header = { 'X-Application' : APP_KEY, 'X-Authentication' : SESSION_TOKEN,'content-type' : 'application/json' }

## Requests list of football events between selected dates.
## eventTypeIds is the id of event type.
json_req_football_events='{"filter":{ "eventTypeIds": ["'+footballID+'"], "marketStartTime": {"from": "'+START_DATE+'", "to": "'+END_DATE+'"} }}'

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

## When printed, returns list of football matches between selected dates. 
football_events_response = requests.post(football_events_url, data=json_req_football_events, headers=header)
## Converts response to json.
formatted_football_events = json.loads(football_events_response.text)
##number_of_events = len(formatted_football_events)
## for each event...
for event in formatted_football_events:
    ## if the event name is equal to sought for event...
    if event['event']['name'] == match_sought_for:
        print("Event Found!")
        ## get the ID of that event.
        eventID = event['event']['id']
        print("Event ID: " + eventID)

## Requests market information for selected match.   
## eventIDs is the id of the match
json_req_football_match='{"filter":{ "eventIds": ["'+eventID+'"] }, "maxResults": "200", "marketProjection": ["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "RUNNER_DESCRIPTION", "RUNNER_METADATA", "MARKET_START_TIME"]}'

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

## When printed, returns list of markets for selected match.
football_match_markets_response = requests.post(football_match_url, data=json_req_football_match, headers=header)
## Converts response to json.
formatted_match_markets = json.loads(football_match_markets_response.text)
## for each market...
for market in formatted_match_markets:
    ## if the market name is equal to sought for market...
    if market['marketName'] == "Match Odds":
        print("Market Found!")
        ## get the ID of that market.
        marketID = market['marketId']
        print("Market ID: " + marketID)

## Requests odds for selected market of the match.
## market id is id of market for that match
json_req_market_odds='{"marketIds": ["'+marketID+'"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true" }}'

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

##json_req_place_bet='{
##[
##    {
##        "jsonrpc": "2.0",
##        "method": "SportsAPING/v1.0/placeOrders",
##        "params": {
##            "marketId": "1.109850906",
##            "instructions": [
##                {
##                    "selectionId": "237486",
##                    "handicap": "0",
##                    "side": "LAY",
##                    "orderType": "LIMIT",
##                    "limitOrder": {
##                        "size": "2",
##                        "price": "3",
##                        "persistenceType": "LAPSE"
##                    }
##                }
##            ]
##        },
##        "id": 1
##    }
##]

## When printed, returns odds for selected market.
match_market_response = requests.post(match_market_url, data=json_req_market_odds, headers=header)

## Prints list of football events
##print(json.dumps(json.loads(football_events_response.text), indent=3))
## Prints football match info
print(json.dumps(json.loads(football_match_markets_response.text), indent=3))
## Prints odds for market
##print(json.dumps(json.loads(match_market_response.text), indent=3))
##y = json.loads(match_market_response.text)
##print(y[0]['status'])
