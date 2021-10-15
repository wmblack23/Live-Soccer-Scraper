# Live-Football-Scraper (Soccer)
### This is a webscraping program that will return the upcoming game schedule, as well as live and finished scores, for (basically) any football league in the world, straight to your terminal

---
Some notes if you download the program to run on your computer:

1. You will need to install Beautiful Soup and Requests if not already installed:

    `pip install beautifulsoup4`
    
    `pip install requests`
    
2. [The website being scraped](https://www.bbc.com/sport/football/scores-fixtures) only shows fixtures +/- 14 days from the current date.  So, if you're trying to view fixtures a month away, nothing will be returned. 
    
3. There is a list titled *leagues* on line 169.  Fill this list in with all of the leagues that you want to include in your version of the program.  

    For me, as an example, *leagues* looks like = ["English Premier League", "Spanish La Liga", 'Italian Serie A", "French Ligue 1", "German Bundesliga", "Champions League"].  
    
    **Check *League_Names.py* to see all available leagues to choose from.**

4. To download the file, click the green "Code" button in the top right and select "Download ZIP".  Save the file to your PC, navigate to where it's located in the terminal or command line, and run it like below:

![ezgif com-gif-maker (3)](https://user-images.githubusercontent.com/69558085/134715220-714d270e-0dd3-453a-b216-9636508353d2.gif)

The program will automatically detect your timezone and adjust the gametimes accordingly.

## Enjoy!
*Michael Black*

