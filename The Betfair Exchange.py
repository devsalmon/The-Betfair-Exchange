#The Betfair Exchange
import requests
import json
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
APP_KEY = 'iym7OLs6r9EYcFYv'
SESSION_TOKEN = '53LzHqVrx568a+Ex/r6ws9KoPOwNhwWtqgt1trLi3xQ='
footballID = "1"
eventID = ''
marketID = ''
selectionID = ''
START_DATE = "2021-06-01T08:00:00Z"
END_DATE = "2021-06-01T23:00:00Z"
football_events_url = endpoint + "listEvents/"
football_match_url = endpoint + "listMarketCatalogue/"
match_market_url = endpoint + "listMarketBook/"
place_orders_url = endpoint + "placeOrders/"

match_sought_for = input("Football Match: ")
runner_selection = input("Who to Lay/Back: ")
LAY_or_BACK = (input("Lay or Back " + runner_selection + "? ")).upper()

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
        marketID = str(market['marketId'])
        print("Market ID: " + marketID)
        ## Get runner selection ID
        for runner in market['runners']:
            ## If runner is equal to name sought for...
            if runner['runnerName'] == runner_selection:
                print("Runner Found!")
                ## Get the ID of selection.
                selectionID = str(runner['selectionId'])

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

## When printed, returns odds for selected market.
market_details_response = requests.post(match_market_url, data=json_req_market_odds, headers=header)
## Converts response to json.
formatted_market_details = json.loads(market_details_response.text)
## for each market...
##for market in formatted_match_markets:
##    ## if the market name is equal to sought for market...
##    if market['marketName'] == "Match Odds":
##        print("Market Found!")
##        ## get the ID of that market.
##        marketID = market['marketId']
##        print("Market ID: " + marketID)

## Requests to place a bet for selected market.
json_req_place_bet='{"marketId": "'+marketID+'", "instructions": [{"selectionId": "'+selectionID+'","handicap": "0", "side": "'+LAY_or_BACK+'", "orderType": "LIMIT", "limitOrder": {"size": "0.10", "price": "7.0", "persistenceType": "LAPSE"}}]}'

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

## Places a bet and when printed, returns placeOrder response.
req_bet_response = requests.post(place_orders_url, data=json_req_place_bet, headers=header)
## Converts response to json.
formatted_req_bet = json.loads(req_bet_response.text)
print(formatted_req_bet)

## Prints list of football events
##print(json.dumps(json.loads(football_events_response.text), indent=3))
## Prints football match info
##print(json.dumps(json.loads(football_match_markets_response.text), indent=3))
## Prints odds for market
##print(json.dumps(json.loads(market_details_response.text), indent=3))
##y = json.loads(match_market_response.text)
##print(y[0]['status'])
