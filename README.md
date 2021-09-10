# Live-Football-Scraper (Soccer)
### This is a webscraping program that will return the upcoming game schedule, as well as live and finished scores, for (basically) any football league in the world, straight to your terminal

---
Some notes if you download the program to run on your computer:

1. You will need to install Beautiful Soup if not already installed:

    `pip install beautifulsoup4`
    
2. There is a list titled *leagues* on line 85.  Fill this list in with all of the leagues that you want to include in your version of the program.  

    For me, as an example, *leagues* looks like = ["English Premier League", "Spanish La Liga", 'Italian Serie A", "French Ligue 1", "German Bundesliga", "Champions League"].  
    
    **Check *League_Names.py* to see all available league names to choose from.**
3. The site I scraped (BBC) shows times for the UK, so you will need to adjust the time +/- the difference between where you live and the UK.  

      a. There is a variable titled *hours_diff* on line 157.  Set this variable equal to the number of hours your timezone is different from the UK (absolute value).
 
      b. There is a variable titled *minutes_diff* on line 158.  Do the same, for minutes difference.
      
      **The program is set for US EST, so if that is not your timezone it will need to be changed**
      
      c. Then, on line 159, you'll add/subtract the *hours_diff* and *minutes_diff* variables.
      
      d. REFER TO THE PICTURE BELOW
      
      ![Screen Shot 2021-09-10 at 10 49 25 AM 1](https://user-images.githubusercontent.com/69558085/132873046-a414cb90-4399-4d7c-b7d5-2811cd215b5a.png)

      
      I live in US EST, so I subtract 5 hours and 0 minutes from the UK time!
4. To download the file, click the green "Code" button in the top right and select "Download Zip".  Save the file to your PC, access it through the terminal or command line, and run it like below:

![Screen Shot 2021-09-10 at 9 23 31 AM](https://user-images.githubusercontent.com/69558085/132860335-b353a012-1b9e-45dd-8dd8-091ec6d3275a.png)
