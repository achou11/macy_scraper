# Important Info:

## 1. Dependencies:
- This is what I used, although the app should work fine with slightly earlier versions of these dependencies. NOTE: Python 3.6.X is the only exception to this, since f-strings are used for the console output in the scraper. **Use Python 3.6.X**

- ### Python 3.6.2
Packages & modules used:  
> pymongo 3.5  
> selenium 3.5.0  
> re 2017.4.5

- ### Node 6.11.2
Packages and modules used:
> express: 4.15.4  
> mongoose: 4.11.6  

- ### MongoDB 3.4

- ### Google Chrome
> Be sure to have Selenium Chromedriver installed

## 2. Running the app
- All commands are from a unix-based command line. Sorry Windows people :/  

- Run `npm install` to load necessary Node modules and packages    

- Go to `macy_scraper` directory i.e. `cd ~/path/to/macy_scraper`  

- Type `mongod` to start the Mongo server. This will run for the duration of the app. The app uses the default /data/db directory for the database.

- Type `python selenium_scraper.py` to run the scraping script. A new instance of your Chrome browser will open up and automation will begin.   

- Once the scraper script is finished (Chrome instance will close and console output will indicate this), type `node app.js` to run the local http server. The server uses the localhost and runs on port 3000.  

- Go to `localhost:3000/home` to view the http GET response, which returns each item as a JSON object with relevant information.
