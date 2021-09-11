# Live-Football-Scraper (Soccer)
### This is a webscraping program that will return the upcoming game schedule, as well as live and finished scores, for (basically) any football league in the world, straight to your terminal

---
Some notes if you download the program to run on your computer:

1. You will need to install Beautiful Soup and Requests if not already installed:

    `pip install beautifulsoup4`
    
    `pip install requests`
    
2. [The website being scraped](https://www.bbc.com/sport/football/scores-fixtures) only shows fixtures +/- 14 days from the current date.  So, if you're trying to view fixtures a month away, nothing will be returned. 
    
3. There is a list titled *leagues* on line 85.  Fill this list in with all of the leagues that you want to include in your version of the program.  

    For me, as an example, *leagues* looks like = ["English Premier League", "Spanish La Liga", 'Italian Serie A", "French Ligue 1", "German Bundesliga", "Champions League"].  
    
    **Check *League_Names.py* to see all available leagues to choose from.**
4. The site I scraped (BBC) shows times for the UK, so you will need to adjust the time +/- the difference between where you live and the UK.  

      a. There is a variable titled *hours_diff* on line 154.  Set this variable equal to the number of hours your timezone is different from the UK.
 
      b. There is a variable titled *minutes_diff* on line 155.  Do the same, for minutes difference.
      
      **The program is set for US EST, so if that is not your timezone it will need to be changed.**
      
      c. Then, on line 160, you'll add/subtract the *hours_diff* and *minutes_diff* variables.
      
      d. REFER TO THE PICTURE BELOW
      
      ![Screen Shot 2021-09-10 at 7 53 16 PM](https://user-images.githubusercontent.com/69558085/132928646-3015ece6-0e60-4543-aa92-124c08cc1504.png)


      
      I live in US EST, so I subtract 5 hours and add/subtract 0 minutes from the UK time.
5. To download the file, click the green "Code" button in the top right and select "Download ZIP".  Save the file to your PC, navigate to where it's located in the terminal or command line, and run it like below:

![Screen Shot 2021-09-10 at 9 23 31 AM](https://user-images.githubusercontent.com/69558085/132860335-b353a012-1b9e-45dd-8dd8-091ec6d3275a.png)
