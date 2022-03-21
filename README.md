# HCDE 310 Final Project - Au21
Final project for HCDE 310 - Autumn 2021 @UW

# Description
**PlayList🕹** is a site that allows users to find, organize, and get information about video games of interest.

Key features:
- Compiles useful information such as game genre, playtime, pricing, and review scores with different APIs across multiple sources
- Autocomplete/suggest games based on user input
- Simple & intuitive UI with responsive design

# Context
The project was built near the end of Autumn quarter 2021 in approximately 2.5~3 weeks.

While I strive to maintain high code quality, I am aware that some programming decisions around performance, modularity, and code clarity could be improved & optimized. This is due to time constraints and the nature of the project being an interactive prototype.

# Live demo
~~http://playlist2.azurewebsites.net
(Website may take up to 2 minutes to load from cold start)~~

(Live demo is temporarily unavailable due to expired API keys)

# File structures
All React TypeScript files are contained in `front-end` folder.

Back-end Python code files are in the root directory (`application.py` is the main file) 


# Usage
1. Install the necessary packages listed in `requirements.yml`.

2. Install Node.js to build the React app
    Start from the root directory of the repo, run the following commands in Terminal. This will install the necessary packages.
    ```
    cd front-end
    npm install
    ```

3. Obtain API keys for IGDB and IsThereAnyDeal from the links below. 

    For the program to have access to the necessary data sources, create a file called `keys.py` under the root directory of the repo. Then save your API keys in the following format.

    ```
    IGDB_ID = 'IGDB ID'
    IGDB_secret = 'IGDB secret'
    ITAD_key = 'IsThereAnyDeal API key'
    ```

4. Start Python Flask server

    Run the code in `application.py` either in your IDE
    
    **OR**
    
     Run the following command in Terminal from the root directory of the repo:
     ```
     python application.py
     ```


5. Start React server
    
    Start from the root directory of the repo, run the following commands in Terminal to start a development server for the front end application.
    ```
    cd front-end
    npm start
    ```
    Instead of `npm start`, you can also run [other commands/scirpts](https://create-react-app.dev/docs/available-scripts).

6. When you're done. Press Control-C or the stop button to stop Flask/React server individually.


# APIs & Data sources

- [IsThereAnyDeal.com API](https://itad.docs.apiary.io/#)
- [IGDB API](https://www.igdb.com/api)
- [OpenCritic API](https://app.swaggerhub.com/apis-docs/OpenCritic/OpenCritic-API/0.1.0#/Search/searchGames)
- [HowLongToBeat](https://howlongtobeat.com/)

# Third-party code usage

The project contains code from:
- [IGDB API Python Wrapper](https://github.com/twitchtv/igdb-api-python).
- [Unofficial HowLongToBeat Python API](https://github.com/JaeguKim/HowLongToBeat-Python-API)

Note: The unofficial HowLongToBeat Python API includes a webscraper. It is used here for the sole purpose of academics & learning. Consider contact [HowLongToBeat](https://howlongtobeat.com/) or use an alternate data source.

# Disclaimer:

This project is NOT affiliated with any of the above parties.