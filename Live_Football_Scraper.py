#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import date
import os, pytz, datetime, re
import time as mytime


# In[ ]:


"""
Function to swap item positions in a list. Called later
"""
################################################################################
def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]


# In[ ]:


refresh = ''
first_go = 0

while refresh == '': # Continuous loop to refresh the live scores
    
    """
    First loop to select the date of the fixtures to view
    """
    ################################################################################

    if first_go == 0:

        Today = date.today()
        print(' ')
        date_to_look = input('Enter a date (YYYY-MM-DD) to view the matches in your selected leagues: ')
        
        match = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_to_look)
        is_match = bool(match)
        
        if is_match == False:
            os.system("clear")
            print("Invalid entry. Make sure your date is entered in ('YYYY-MM-DD') format: ")
            continue
        
        year, month, day = (int(x) for x in date_to_look.split('-'))    
        ans = datetime.date(year, month, day)

        print(' ')
        print('-'*100)
        print('-'*100)
        print(' ')
        print('Matchups in the following leagues for {}, {} {}, {}:'.format(ans.strftime("%A"),
                                                                              ans.strftime("%B"),
                                                                              ans.strftime("%d"), 
                                                                                  ans.strftime("%Y")))
        print(' ')
            
        
        
    first_go += 1
    
    from datetime import datetime
        
    """
    Web scraping code
    """
    ###############################################################################
    
    url = "https://www.bbc.com/sport/football/scores-fixtures/" + str(date_to_look)

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "html.parser")
        

    leagues = (['English Premier League', 'Spanish La Liga',  'German Bundesliga',  'Italian Serie A', 
            'French Ligue 1', 'Champions League'])
        
    tags = ["span", "h3"]
    classes = (["gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc",
                  "sp-c-fixture__status-wrapper qa-sp-fixture-status",
                  'sp-c-fixture__number sp-c-fixture__number--time', "sp-c-fixture__number sp-c-fixture__number--home",
                  "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft",
                 "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport",
                  "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live-sport",
                 "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft",
                  'gel-minion sp-c-match-list-heading'])

    scraper = soup.find_all(tags, attrs={'class': classes})

    data = [str(l) for l in scraper]
    
    """
    Changing all instances of 'Premier League' to 'English Premier League' for better consistency
    """
    ################################################################################

    prem_header = ">Premier League</h3>"
    EPL_header = ">English Premier League</h3>"
    prem_span = "$0Premier League"
    EPL_span = "$0English Premier League"

    for i in data:
        if prem_header in i:
            data[data.index(i)] = data[data.index(i)].replace(prem_header, EPL_header)
        elif prem_span in i:
            data[data.index(i)] = data[data.index(i)].replace(prem_span, EPL_span)
        else:
            i
    
    """
    Getting rid of unnecessary string data. Cutting it to just what we need
    """
    ################################################################################
    
    data = [i[-145:] for i in data]
    left, right = '">', '</'
    data = [[l[l.index(left)+len(left):l.index(right)] for l in data if i in l] for i in leagues]

    """
    The purpose of this loop is to add an '(H)' after the home team's name and an '(A)' after the away teams'.
    This is for games that have yet to be played. The function swap_positions is called to swap the game-time to
    AFTER the '(A)'. So order for an upcoming game is 'Home team, (H), Away team, '(A), gametime'
    """
    ################################################################################
    
    for i in data:
        while '' in i:
            swap_positions(i, i.index(''), i.index('') - 2)
            blank = i.index('')
            blank_2 = i.index('') + 2
            i[blank] = '(H)'
            i.insert(blank_2, '(A)')

         
    """
    Changing the match-time from UK time to your local time, whatever that may be.
    """
    ################################################################################
    
    data = [l for l in data if len(l) != 0]
    
    curr_time = mytime.localtime()
    curr_clock = mytime.strftime("%Y:%m:%d %H:%M:%S %Z %z", curr_time)

    IST = pytz.timezone('Europe/London')
    datetime_ist = datetime.now(IST)
    london = datetime_ist.strftime("%Y:%m:%d %H:%M:%S %Z %z")

    curr_hour, curr_min = curr_clock[-5:-2], curr_clock[14:16]

    lndn_hour, lndn_min = london[-5:-2], london[14:16]

    hour_diff = int(lndn_hour) - int(curr_hour)
    min_diff = int(lndn_min) - int(curr_min)

    if min_diff == 0:
        min_diff = str(min_diff) + '0'

    for k in data:
        for indx, item in enumerate(k):
        
            if ":" in item:

                if min_diff == '00':
                    val = str(int(item[:item.index(":")]) - hour_diff) + item[item.index(":"):]

                if min_diff != '00':
                    val = str(int(item[:item.index(":")]) - hour_diff) + ":" + str(abs(min_diff) + int(item[item.index(":") + 1:]))

                if int(val[val.index(":") + 1:]) >= 60:
                    val = str(int(val[:val.index(":")]) + 1) + ":" + str(int(val[val.index(":") + 1:]) - 60)

                if int(val[:val.index(":")]) >= 24:
                    val = str(int(val[:val.index(":")]) -24) + "0:" + str(int(val[val.index(":") + 1:])) + " +1"

                if val[val.index(":") + 1:] == '0':
                    val = i + '0'

                try:
                    if int(val[val.index(":") + 1:]) < 10 and int(val[val.index(":") + 1:]) > 0:
                        colon = val.find(":")
                        val = val[:colon + 1] + '0' + val[colon + 1:]
                except ValueError:
                        k[indx] = val
                        continue


                k[indx] = val
    
    data = [[i.replace('&amp;', '&') for i in group] for group in data] # Brighton & Hove Albion problem

    """
    Final print loop
    """
    ################################################################################
    
    no_games = all(len(l) == 0 for l in data)
    
    if (no_games):
        print('NO GAMES ON THIS DATE')
        break
    
    ct = 0
    league_in = 0
    h_team, h_score, a_team, a_score, time = 1, 2, 3, 4, 5

    for i in data:

        print(i[0])
        print('-'*25)

        while ct < len(data[league_in][1:]) // 5:
            print("{:<25} {:^5} {:<25} {:^3} | {:>7}".format(i[h_team], i[h_score], i[a_team], i[a_score], i[time]))
            ct += 1
            h_team += 5
            h_score += 5
            a_team += 5
            a_score += 5
            time += 5

        print(' ')
        league_in += 1
        ct, h_team, h_score, a_team, a_score, time = 0, 1, 2, 3, 4, 5
    
    """
    Refresh the page to view updated scores.
    Clear the old scores from the terminal
    """
    ################################################################################
    
    refresh = input('Press "Enter" to refresh the page: ')
    os.system("clear")

