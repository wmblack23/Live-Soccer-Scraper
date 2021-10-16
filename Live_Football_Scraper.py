#!/usr/bin/env python
# coding: utf-8

# Notebook scrapes fixture data from: https://www.bbc.com/sport/football/scores-fixtures

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import date as mydate
from datetime import datetime as mydatetime
import os, pytz, datetime, re
import time as mytime


# In[ ]:


def swap_positions(list, pos1, pos2):
    
    """
    Function to swap item positions in a list.
    
    Called later
    """
    
    list[pos1], list[pos2] = list[pos2], list[pos1]


# In[ ]:


def clean_data(list):
    
    """
    Changing all instances of 'Premier League' to 'English Premier League' for better consistency.
    Also chops away all unnecessary string data.
    
    Called later
    """
    
    prem_header = ">Premier League</h3>"
    EPL_header = ">English Premier League</h3>"
    prem_span = "$0Premier League"
    EPL_span = "$0English Premier League"

    for indx, item in enumerate(list):
        if prem_header in item:
            list[indx] = list[indx].replace(prem_header, EPL_header)
        elif prem_span in item:
            list[indx] = list[indx].replace(prem_span, EPL_span)
        else:
            item

    leagues = (['English Premier League', 'Spanish La Liga',  'German Bundesliga',  'Italian Serie A', 
            'French Ligue 1', 'Champions League'])
    
    list = [i[-145:] for i in list]
    left, right = '">', '</'
    list = [[l[l.index(left)+len(left):l.index(right)] for l in list if i in l] for i in leagues]
    
    return list


# In[ ]:


def home_and_away(list):
    
    """
    For games that haven't occured yet, our scraper will return Home Team, Away Team, and game time.
    There will be an empty spot '' where our scraper tried to scrape the minute the game is in, but since
    the game has yet to start it is empty.
    
    This function fills the blank space with an (H) to signify home team, then creates a new blank space
    and fills it with an (A) to signify away team, and re-orders the list so it reads:
    
    'Home Team, (H), Away Team, (A), Game time'
    
    Called later
    """
    
    for i in list:
        while '' in i:
            swap_positions(i, i.index(''), i.index('') - 2)
            blank = i.index('')
            blank_2 = i.index('') + 2
            i[blank] = '(H)'
            i.insert(blank_2, '(A)')
            


# In[ ]:


def choose_date():
    
    """
    User inputs the date they would like to check
    If input is in the wrong format, user is prompted to try it again
    """
    
    print_once = True
    while print_once:

        print(' ')
        date_to_look = input('Enter a date (YYYY-MM-DD) to view the matches in your selected leagues: ')

        match = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_to_look)
        is_match = bool(match) # Check if date was entered wrong

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

        print_once = False
        
    return str(date_to_look)


# In[ ]:


def scraping():
    
    """
    Web scraping code
    """
    
    url = "https://www.bbc.com/sport/football/scores-fixtures/" + date_to_choose

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "html.parser")
        
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
    
    data = clean_data(data) # Functiom call
    home_and_away(data)     # Function call
    
    data = [l for l in data if len(l) != 0]
    
    return data


# In[ ]:


def change_time():
    
    """
    Alters match-time from UK time (site gives games in UK time) to whatever the local time is
    by detecting users timezone automatically
    """
    
    data = scraping() # Function call

    curr_time = mytime.localtime()
    curr_clock = mytime.strftime("%Y:%m:%d %H:%M:%S %Z %z", curr_time)

    IST = pytz.timezone('Europe/London')
    datetime_ist = mydatetime.now(IST)
    london = datetime_ist.strftime("%Y:%m:%d %H:%M:%S %Z %z")

    curr_hour, curr_min = curr_clock[-5:-2], curr_clock[14:16]
    lndn_hour, lndn_min = london[-5:-2], london[14:16]
    
    # Comparing time difference between London and user's local time
    hour_diff = int(lndn_hour) - int(curr_hour)
    min_diff = int(lndn_min) - int(curr_min)

    if min_diff == 0:
        min_diff = str(min_diff) + '0'

    for k in data:
        for indx, item in enumerate(k):
        
            if ":" in item:
    
                if min_diff == '00': # If there is no minute difference, change hours and keep minutes the same
                    val = str(int(item[:item.index(":")]) - hour_diff) + item[item.index(":"):]

                if min_diff != '00': # If there is a minutes difference, change hours and minutes
                    val = str(int(item[:item.index(":")]) - hour_diff) + ":" + str(abs(min_diff) + int(item[item.index(":") + 1:]))

                if int(val[val.index(":") + 1:]) >= 60: 
                    # If the new 'minutes' value is >= 60, add 1 to the hour value and subtract 60 from the minutes
                    val = str(int(val[:val.index(":")]) + 1) + ":" + str(int(val[val.index(":") + 1:]) - 60)

                if int(val[:val.index(":")]) >= 24:
                    # If the new hours value is >= 24, subtract 24 from the hours and add a '+1' to the end
                    # to signify game is taking place the following day
                    val = "0" + str(int(item[:item.index(":")]) -24) + ":" + str(int(item[item.index(":") + 1:])) + " +1"

                if val[val.index(":") + 1:] == '0':
                    val = i + '0' # Add a second '0' to minutes value is there is only one

                try:
                    # If minutes value is between 1-9, add a '0' so that it reads '11:07' rather than
                    # '11:7', for example
                    if int(val[val.index(":") + 1:]) < 10 and int(val[val.index(":") + 1:]) > 0:
                        colon = val.find(":")
                        val = val[:colon + 1] + '0' + val[colon + 1:]
                except ValueError:
                        k[indx] = val
                        continue
                k[indx] = val
    
    data = [[i.replace('&amp;', '&') for i in group] for group in data] # Brighton & Hove Albion problem
    
    return data


# In[ ]:


def final_print():
    
    """
    Final print function
    
    If user presses Enter while in terminal the scores will refresh without the user needing to enter
    the date to search again. This way it can be called once during matchdays and work throughout the day
    """
    
    refresh = ''
    
    while refresh == '':
        
        ct = 0
        league_in = 0
        h_team, h_score, a_team, a_score, time = 1, 2, 3, 4, 5
        
        data = change_time()
       
        no_games = all(len(l) == 0 for l in data)
        if (no_games): # If all the lists are empty
            print('NO GAMES ON THIS DATE')
            break

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
            
        refresh = input('Press "Enter" to refresh the page: ')
        os.system("clear")
        


# In[ ]:


if __name__ == "__main__":
    date_to_choose = choose_date()
    final_print()


# In[ ]:




