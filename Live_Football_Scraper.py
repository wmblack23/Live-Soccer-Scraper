#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import os


# In[27]:


"""
Function to swap item positions in a list. Called later
"""
################################################################################
def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]

"""
Function to account for the time zones that have different minutes and hours both
"""
def fix_time(time):
    
    start = time[:time.index(":")]
    end = time[time.index(":")+1:]
    
    new_time = str(int(start) + 1) + ":" + str(int(end) - 60)
    
    if new_time[-2:] == ":0":
        new_time = new_time + '0'
    
    return new_time


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
        
    """
    Web scraping code
    """
    ###############################################################################
    
    url = "https://www.bbc.com/sport/football/scores-fixtures/" + str(date_to_look)

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")
        

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
    ct = 0
    for i in data:
        if prem_header in i:
            data[ct] = data[ct].replace(prem_header, EPL_header)
            ct += 1
        elif prem_span in i:
            data[ct] = data[ct].replace(prem_span, EPL_span)
            ct += 1
        else:
            ct += 1
    
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
    
    ct = 0
    while ct < len(data):
        if '' in data[ct]:
                while '' in data[ct]:
                    swap_positions(data[ct], data[ct].index(''), data[ct].index('') - 2)
                    blank = data[ct].index('')
                    blank_2 = data[ct].index('') + 2
                    data[ct][blank] = '(H)'
                    data[ct].insert(blank_2, '(A)')
                ct += 1
        else:
            ct += 1
         
    """
    Because the site scraped was BBC, the times are UK times. I subtract 5 hours to make it US EST kickoff.
    The for-loop accounts for time zones where the minutes are also different, not just the hours.
    """
    ################################################################################
    
    hours_diff = 5
    minutes_diff = 0
    data = [[str((int(l[:2]) - hours_diff)) + ":" + (str(int(l[3:]) + minutes_diff)) if ":" in l else l for l in group] for group in data]
    
    for i in data:
        for k in i:
            if ":" in k and int(k[k.index(":")+1:]) >= 60:
                i[i.index(k)] = fix_time(k)
    
    data = [l for l in data if len(l) != 0]
    data = [[i.replace('&amp;', '&') for i in group] for group in data] # Brighton & Hove Albion problem
    
    """
    Adding a zero to the end of the gametimes when needed
    """
    ################################################################################
    
    ct = 0
    while ct < len(data):
        for i in data[ct]:
            if i[-2:] == ':0':
                data[ct][data[ct].index(i)] = data[ct][data[ct].index(i)] + '0'
        ct += 1    
    
    """
    Final print loop
    """
    ################################################################################
    
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


# In[ ]:




