#Finds lowest lay draw odds.
import requests
import json
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
APP_KEY = 'iym7OLs6r9EYcFYv'
SESSION_TOKEN = '53LzHqVrx568a+Ex/r6ws9KoPOwNhwWtqgt1trLi3xQ='
footballID = "1"
eventID = ''
marketID = ''
selectionID = ''
##GMT is UK time - 1 hour.
START_DATE = "2021-06-01T00:00:00Z"
END_DATE = "2021-06-01T23:59:59Z"
football_events_url = endpoint + "listEvents/"
football_match_url = endpoint + "listMarketCatalogue/"
match_market_url = endpoint + "listMarketBook/"
place_orders_url = endpoint + "placeOrders/"
header = { 'X-Application' : APP_KEY, 'X-Authentication' : SESSION_TOKEN,'content-type' : 'application/json' }

lay_draw_odds_list = []
number_of_bets_today = 0

## Requests list of football events between selected dates.
## eventTypeIds is the id of event type.
json_req_football_events='{"filter":{ "eventTypeIds": ["'+footballID+'"], "marketStartTime": {"from": "'+START_DATE+'", "to": "'+END_DATE+'"} }}'

## When printed, returns list of football matches between selected dates. 
football_events_response = requests.post(football_events_url, data=json_req_football_events, headers=header)
## Converts response to json.
formatted_football_events = json.loads(football_events_response.text)
##number_of_events = len(formatted_football_events)

## for each event...
for event in formatted_football_events:

    ## get the ID of the event.
    eventID = event['event']['id']
    print(event['event']['name'])
    ## Then request list of markets for each match.   
    ## eventIDs is the id of the match
    json_req_football_match='{"filter":{ "eventIds": ["'+eventID+'"] }, "maxResults": "200", "marketProjection": ["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "RUNNER_DESCRIPTION", "RUNNER_METADATA", "MARKET_START_TIME"]}'
    ## (When printed, returns list of markets for selected match.)
    football_match_markets_response = requests.post(football_match_url, data=json_req_football_match, headers=header)
    ## (Converts response to json.)
    formatted_match_markets = json.loads(football_match_markets_response.text)

    ## for each market of the current match...
    for market in formatted_match_markets:
        
        ## check the market name is equal to sought for market...
        if market['marketName'] == "Match Odds":
            print("Market Found!")
            ## Then get the ID of that market.
            marketID = market['marketId']
            
            ## Then get the selection ID for The Draw.
            ## from either home win, draw or away win, get id for draw.
            for runner in market['runners']:
                
                ## If runner name (the thing we are betting on) is equal to the draw... 
                if runner['runnerName'] == "The Draw":
                    print("The Draw Found!")
                    ## Get the ID of that selection.
                    selectionID = runner['selectionId']
                    ## We then need to get odds for that selection.
                    ## First request all odds for selected market of the match.
                    ## (market id is id of market for that match)
                    json_req_market_odds='{"marketIds": ["'+marketID+'"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true" }}'
                    ## (When printed, returns odds for selected market.)
                    market_details_response = requests.post(match_market_url, data=json_req_market_odds, headers=header)
                    ## (Converts response to json.)
                    formatted_market_details = json.loads(market_details_response.text)

                    ## Then obtain odds for laying draw.
                    ## From either win, draw or away, get selectionID that matches draw.
                    for outcome in formatted_market_details[0]['runners']:

                        ## Check that odds are for draw.
                        if outcome['selectionId'] == selectionID:
                            ## Get best lay price if it exists.
                            if outcome['ex']['availableToLay'][0]['price']:
                                best_lay_price = outcome['ex']['availableToLay'][0]['price']
                                ## Get the available size to lay.
                                available_lay_size = outcome['ex']['availableToLay'][0]['size']
                                print("Lay draw odds: " + str(best_lay_price))
                                ## Adds best odds to the list.
                                lay_draw_odds_list.append(best_lay_price)
                                print("Available lay size: " + str(available_lay_size))

print("Lay-draw odds list: ")
print(lay_draw_odds_list)
print("Min lay-draw odds: ")
print(min(lay_draw_odds_list))
print("Index pos of min lay-draw odds: ")
print(lay_draw_odds_list.index(min(lay_draw_odds_list)))
## Requests to place a bet for selected market.
###json_req_place_bet='{"marketId": "'+marketID+'", "instructions": [{"selectionId": "'+selectionID+'","handicap": "0", "side": "'+LAY_or_BACK+'", "orderType": "LIMIT", "limitOrder": {"size": "2", "price": "3.35", "persistenceType": "LAPSE"}}]}'

## When printed, returns placeOrder response.
###req_bet_response = requests.post(place_orders_url, data=json_req_place_bet, headers=header)
## Converts response to json.
###formatted_req_bet = json.loads(req_bet_response.text)
###print(formatted_req_bet)

## Prints list of football events
##print(json.dumps(json.loads(football_events_response.text), indent=3))
## Prints football match info
##print(json.dumps(json.loads(football_match_markets_response.text), indent=3))
##Prints odds for market
##print(json.dumps(json.loads(market_details_response.text), indent=3))
##y = json.loads(match_market_response.text)
##print(y[0]['status'])
