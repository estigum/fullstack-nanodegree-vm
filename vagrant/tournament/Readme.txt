Author: Erik Stigum
Email: estigum@gmail.com
Copyright: Copyright 2015, Swiss Tournament
Version: 1.0

This is my version of the Swiss Tournament for the full-stack nanodegree. 

APPLICATION SUPPORTS
1. Running a single swiss tournament
2. Running multiple swiss tournaments
4. Get Overall standings for a single tournament or over all tournaments.
3. Making sure those who have matched up don't match up again.
4. Support for odd number of players.
5. Generate Web pages for each tournament and overall standings.

DATABASE
tournament.sql - Includes tables to store the date and  stored procedures for retrieving data and
saving data to the database.

TABLES
1. Players - This has the list of players in the tournament
2. SwissTournament - List of tournaments that are going on.
3. TournamentResults - This is the results for the tournaments.

STORED PROCEDURES
1. update_tournament_round - Updates the current round for a given tournament
2. add_player - This will add a player to the Players table
3. register_swiss_tournament - This will register a new tournament and add a row to
SwissTournament table.
4. report_match - Will report results of a match for a given tournament. Enter a row int
TournamentResults table.
5. get_past_matches - This returns past matches for a given tournament.  This is used to prevent
   people from matching up again.
6. get_player_standings - This will get player standings for a given tournament or overall for all
tournaments -  You pass in 0 it will give you overall for all the tournaments that happened. If
you only want for a single tournament you pass in the tournamentid.
7. get_swiss_pairings - Returns the pairings for a given tournament

PYTHON FILES
1. tournament.py - This contains all the database calls.  I wanted to break it up and not make this the
main file.
2. tournament_test.py - This is the test cases for tournament.py
2. swisstournament.py - This is the main file that runs the tournaments. It has the main method and a class to
run the tournaments.
3. NoMatch.py - This contains a class to prevent rematches
4. tournamentexception.py - This is a special exception  for the tournament when seeing if the correct
parameters are passed or the config file is correct.

PLAYER FILES
1. players.txt - has 16 players
2. players-odd.txt - has 15 players

CONFIG FILES
1. singletournament.cfg - Runs a single swiss tournament
2. signeltournament-odd.cfg - Runs a single swiss tournament with odd number of players
3. multitournament.cfg - Runs three tournaments.  You can add more.

CONFIG SETTINGS
1. [run_mode] section
   A. tournaments - list of tournaments. Comma separated
   B. player_file - the player file to use
   C. web_support - I will always generate HTML files, but you can have the browser bring them up.  If you want that set this
   to True.  If not set it to False. If running in virtual environment web pages won't come up.  If you run the database native
   you can display the web pages.
   D. output_file - I also output the results to a text file.  You put the name where you want to store the results
2. [logging]
   A. mode - what you want to output.  Different levels.
     1. DEGUG - All logging messages for DEBUG, INFO, WARNING, ERROR
     2. INFO - All logging messages for INFO, WARNING, ERROR
     3. WARNING - All logging messages for WARNING, ERROR
     4. ERROR - Only Error

HTML FORMATTING
1. stylesheet.css - Added styling to the web pages. I create tables for each round. Also
the overall has a table.  Other formatting for background and foreground color. Formatting
for fonts and sizes.

RUN APPLICATION
1. Testing single tournament - even players
  A. python swisstournament.py singletournament.cfg
2. Testing single tournament - odd players
  A. python swisstournament.py singletournament-odd.cfg
3. Testing multi tournament
  A. python swisstournament.py multitournament.cfg
