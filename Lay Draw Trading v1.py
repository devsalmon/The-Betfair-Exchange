#Finds lowest lay draw odds.
import requests
import json
from datetime import datetime
import time
import pytz

run = True

## Will run for 4 days!
while run == True:
    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    #current_time = datetime.datetime.now(pytz.timezone('GMT')).strftime('%Y-%m-%dT%H:%M:%SZ')
    endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
    APP_KEY = 'iym7OLs6r9EYcFYv'
    SESSION_TOKEN = 'UOjhtIsbPLDvphyhxNJsVbleXuZ9KjhjXigJxm7YmdM='
    footballID = "1"
    eventID = ''
    marketID = ''
    selectionID = ''
    ##GMT is UK time - 1 hour.
    START_DATE = "2021-06-06T10:00:00Z"
    END_DATE = "2021-06-07T19:59:59Z"
    football_events_url = endpoint + "listEvents/"
    football_match_url = endpoint + "listMarketCatalogue/"
    match_market_url = endpoint + "listMarketBook/"
    place_orders_url = endpoint + "placeOrders/"
    header = { 'X-Application' : APP_KEY, 'X-Authentication' : SESSION_TOKEN,'content-type' : 'application/json' }

    eventName_list = []
    eventID_list = []
    marketID_list = []
    selectionID_list = []
    lay_draw_odds_list = []
    lay_draw_odds_under_3point5_list = []
    liability_list = []
    available_lay_size_for_U3point5_list = []
    index_of_odds_under_3point5_list = []
    start_time_of_selected_matches_list = []
    number_of_bets_today = 0
    index_pos = -1

    frequent_monitor = False
    difference_in_hours_list = []
    time_until_min_61_list = []

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
        ## Find the difference between when event starts and now.
        difference_in_time = datetime.strptime(event['event']['openDate'], '%Y-%m-%dT%H:%M:%S.000Z') - datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.000Z')
        ## Adds the difference in hours to a list.
        difference_in_hours = difference_in_time.total_seconds() / 3600
        ## Only selectes events that have not started yet.
        if difference_in_hours > 0:
            
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
                                    if outcome['ex']['availableToLay']:
                                        best_lay_price = outcome['ex']['availableToLay'][0]['price']
                                        ## Get the available size to lay.
                                        available_lay_size = outcome['ex']['availableToLay'][0]['size']
                                        print("Lay draw odds: " + str(best_lay_price))
                                        ## Adds best odds to the list.
                                        lay_draw_odds_list.append(best_lay_price)
                                        index_pos += 1
                                        print("Available lay size: " + str(available_lay_size))
                                        ## If odds are low enough...
                                        if best_lay_price <= 3.5: #and available_lay_size > 10:
                                            print("BELLOW 3.5")
                                            ## Adds event name of selected event to list.
                                            eventName_list.append(event['event']['name'])
                                            ## Adds eventID of selected event to list.
                                            eventID_list.append(eventID)
                                            ## Adds marketID of selected market to list.
                                            marketID_list.append(marketID)
                                            ## Adds selectionID of The Draw to list...
                                            selectionID_list.append(selectionID)
                                            ## Adds odds to new list.
                                            lay_draw_odds_under_3point5_list.append(best_lay_price)
                                            ## Adds available lay size for these odds to new list.
                                            available_lay_size_for_U3point5_list.append(available_lay_size)
                                            ## Adds index pos of selected odds to list.
                                            index_of_odds_under_3point5_list.append(index_pos)
                                            ## Adds start times of selected matches to list.
                                            start_time_of_selected_matches_list.append(event['event']['openDate'])
                                            ## Lay the draw with stake £2.
                                            liability = (2 * best_lay_price) - 2
                                            liability_list.append(liability)
                                            ## Adds difference in hours to a list.
                                            difference_in_hours_list.append(difference_in_hours)
                                            ## Adds time until min 61 of match to a list.
                                            time_until_min_61 = difference_in_hours + 1.3
                                            time_until_min_61_list.append(time_until_min_61)
                                            ## Bet Calculations
                                            
    print("Lay-draw odds list: ")
    print(lay_draw_odds_list)
    print("Min lay-draw odds: ")
    print(min(lay_draw_odds_list))
    print("Index pos of min lay-draw odds: ")
    print(lay_draw_odds_list.index(min(lay_draw_odds_list)))
    print("Lay-draw odds under 3.5: ")
    print(lay_draw_odds_under_3point5_list)
    print("Available lay size: ")
    print(available_lay_size_for_U3point5_list)
    print("Index pos of odds under 3.5: ")
    print(index_of_odds_under_3point5_list)
    print("Start time of selected matches: ")
    print(start_time_of_selected_matches_list)
    print("Selected events name lislt: ")
    print(eventName_list)
    print("Event ID list: ")
    print(eventID_list)
    print("Market ID list: ")
    print(marketID_list)
    print("Selection ID list: ")
    print(selectionID_list)
    print("Liability list: ")
    print(liability_list)
    print("Current time: " + current_time)
    print("Difference in time list: ")
    print(difference_in_hours_list)
    print("Time until min 61: ")
    print(time_until_min_61_list)

    ## Gets value of smallest time left until min 61.
    smallest_time_left = min(time_until_min_61_list)
    ## Gets index of smallest time left value.
    index_of_smallest_time_left = time_until_min_61_list.index(smallest_time_left)
    print("Index of smallest time left: " + str(index_of_smallest_time_left))
    time.sleep(smallest_time_left*3600)
    print("I just napped until min 61")

    json_req_market_odds='{"marketIds": ["'+marketID_list[index_of_smallest_time_left]+'"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true" }}'
    market_details_response = requests.post(match_market_url, data=json_req_market_odds, headers=header)
    ## (Converts response to json.)
    formatted_market_details = json.loads(market_details_response.text)
    ## Then obtain min 61 odds for BACKING draw.
    ## From either win, draw or away, get selectionID that matches draw.
    for outcome in formatted_market_details[0]['runners']:
        ## Check that odds are for draw.
        if outcome['selectionId'] == selectionID_list[index_of_smallest_time_left]:
            ## Get best lay price if it exists.
            if outcome['ex']['availableToBack']:
                best_back_price = outcome['ex']['availableToBack'][0]['price']
                ## Get the available size to lay.
                available_back_size = outcome['ex']['availableToBack'][0]['size']
                print("Back draw odds: " + str(best_back_price))
                print("Available back size: " + str(available_back_size))
                ## If backing odds are above what I layed (profit)...
                ## Replace 3.8 with best_back_price.
                if best_back_price >= lay_draw_odds_under_3point5_list[index_of_smallest_time_left]: #and available_back_size > 10:
                    ## Bet Calculations
                    ## Calculates back size for a guaranteed profit.
                    back_size = (lay_draw_odds_under_3point5_list[index_of_smallest_time_left] * 2) / best_back_price
                    print("Back size: " + str(back_size))
                    guaranteed_profit = (back_size * best_back_price) - (back_size + liability_list[index_of_smallest_time_left])
                    print("Guaranteed profit: " + str(guaranteed_profit))
                    ## Writes bet details to text file.
                    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                    f = open("BetTest.txt", "a")
                    f.write("Date: " + current_time + "\n")
                    f.write("Match: " + eventName_list[index_of_smallest_time_left] + "\n")
                    f.write("Liability: " + str(liability_list[index_of_smallest_time_left]) + "\n")
                    f.write("Back price: " + str(best_back_price) + "\n")
                    f.write("Sold for guaranteed profit: " + str(guaranteed_profit) + "\n")
                    f.close()
                    print("Program Working So Far!")
                ## Back price is smaller so we have lost money.
                else:
                    ## Calculates back size for a guaranteed loss.
                    back_size = (lay_draw_odds_under_3point5_list[index_of_smallest_time_left] * 2) / best_back_price
                    guaranteed_loss = (back_size * best_back_price) - (back_size + liability_list[index_of_smallest_time_left])
                    ## Writes bet details to text file.
                    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                    f = open("BetTest.txt", "a")
                    f.write("Date: " + current_time + "\n")
                    f.write("Match: " + eventName_list[index_of_smallest_time_left] + "\n")
                    f.write("Liability: " + str(liability_list[index_of_smallest_time_left]) + "\n")
                    f.write("Back price: " + str(best_back_price) + "\n")
                    f.write("Sold for guaranteed loss: " + str(guaranteed_loss) + "\n")
                    f.close()
                    print("Program Working So Far!")
            ## Remove match from all lists of selected events.
##            time_until_min_61_list.pop(index_of_smallest_time_left)
##            lay_draw_odds_under_3point5_list.pop(index_of_smallest_time_left)
##            available_lay_size_for_U3point5_list.pop(index_of_smallest_time_left)
##            start_time_of_selected_matches_list.pop(index_of_smallest_time_left)
##            eventID_list.pop(index_of_smallest_time_left)
##            marketID_list.pop(index_of_smallest_time_left)
##            selectionID_list.pop(index_of_smallest_time_left)
##            liability_list.pop(index_of_smallest_time_left)
##            difference_in_hours_list.pop(index_of_smallest_time_left)
            ## Recalculates smallest_time_left of updated list.        
            ## smallest_time_left = min(time_until_min_61_list)

    #### while match is past minute 70
    ##while smallest_time_left < -0.15:
    ##    print("Smallest time left: " + str(smallest_time_left))
    ##    ## Gets index of smallest time left value.
    ##    index_of_smallest_time_left = time_until_min_61_list.index(smallest_time_left)
    ##    ## Remove match from all lists of selected events.
    ##    time_until_min_61_list.pop(index_of_smallest_time_left)
    ##    lay_draw_odds_under_3point5_list.pop(index_of_smallest_time_left)
    ##    available_lay_size_for_U3point5_list.pop(index_of_smallest_time_left)
    ##    start_time_of_selected_matches_list.pop(index_of_smallest_time_left)
    ##    eventID_list.pop(index_of_smallest_time_left)
    ##    marketID_list.pop(index_of_smallest_time_left)
    ##    selectionID_list.pop(index_of_smallest_time_left)
    ##    liability_list.pop(index_of_smallest_time_left)
    ##    difference_in_hours_list.pop(index_of_smallest_time_left)
    ##    ## Recalculates smallest_time_left of updated list.        
    ##    smallest_time_left = min(time_until_min_61_list)

    ## Once selected events have been chosen and added to a list, order the list by time.
    #for i in range(len(eventID_list)):
     #   
        ##if datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.000Z') < datetime.strptime(start_time_of_selected_matches_list[i], '%Y-%m-%dT%H:%M:%S.000Z'):
            ##print("Current time is earlier")
        ##else:
            ##print("Current time is later")

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
