# Live-Football-Scraper (Soccer)
### Scrape live scores and upcoming matches from any football league in the world, straight to your terminal
---
This is a webscraping program that will return the upcoming game schedule, as well as live and finished scores, for (basically) any football league globally.

Some notes if you download the program to run on your computer:

1. There is a list titled "lgs" on line 148/149.  Fill this list in with all of the leagues that you want to include in your version of the program.  

    For me, "lgs" looks like = ["Premier League", "Spanish La Liga", 'Italian Serie A", "French Ligue 1", "German Bundesliga", "Champions League"].  
    
    **Check *League_Names.py* to see all available league names to choose from!**
3. The site scraped shows times for the UK, so you will need to adjust the time +/- the difference between where you live and the UK.  

      a. There is a variable titled *hours_diff* on line 194.  Set this variable equal to the number of hours your timezone is different from the UK (absolute value).
 
      b. There is a variable titled *minutes_diff* on line 195.  Do the same, for minutes difference.
      
      c. Then, on line 196, you'll add/subtract the *hours_diff* and *minutes_diff* variables.
      
      d. **REFER TO THE PICTURE BELOW**
      ![Screen Shot 2021-09-09 at 9 43 12 PM](https://user-images.githubusercontent.com/69558085/132785517-92b928eb-452b-4ca0-bcda-d4b71be61dc9.png)
      
      I live in US EST, so I subtract 5 hours and 0 minutes from the UK time!
