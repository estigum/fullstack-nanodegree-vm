#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import NoMatch


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(db=None, tournamentid=None):
    """Remove all the match records from the database."""
    if not db:
        db = connect()

    sql_text = ""
    if not tournamentid:
        sql_text = "delete from TournamentResults"
    else:
        sql_text = "delete from TournamentResults where tournamentId=" + str(tournamentid)

    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def deletePlayers(db=None):
    """Remove all the player records from the database."""

    if not db:
        db = connect()
    sql_text="delete from Players"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()


def countPlayers(db=None):
    """Returns the number of players currently registered."""

    if not db:
        db = connect()
    sql_text="select count(*) from Players"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    for row in rows:
        return row[0];
    return 0

def getPlayers(db):
    """
    This will get all players that will participate
    in Swiss tournament
    :param db:
    :return list of players:
    """
    sql_text="select * from Players"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    return rows

def registerSwissTournament(name, db=None):
    """
    This will register a new Swiss Tournament
    Allows you to run multiple tournaments
    :param name:
    :param db:
    :return:
    """
    if not db:
        db = connect()
    sql_text="select register_swiss_tournament('" + name +"')"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def getPastMatchesForTournament(db, tournamentid):
    """
    This gets all past matches for a given tournament.
    This is needed to determin if someone has already
    had a match
    :param db:
    :param tournamentid:
    :return list of matchups:
    """
    sql_text="select winnerid, loserid from TournamentResults where tournamentid=" + str(tournamentid)
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    return rows

def getSwissTournamentId(name, db=None):
    """
    This will get the tournamentid for a given
    Swiss Tournament name.
    :param name:
    :param db:
    :return id of swiss tournamanent:
    """
    if not db:
        db = connect()
    sql_text="select id from SwissTournament where name='" + name +"'"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    for row in rows:
        return row[0]
    return 0

def updateSwissTournamentRound(tournament_id,round, db=None):
    """
    Update the round the swiss tournament is in.
    :param tournament_id:
    :param round:
    :param db:
    :return:
    """
    if not db:
        db = connect()
    sql_text="Update SwissTournament set rounds=" + str(round) + " where id=" + str(tournament_id)
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def deleteSwissTournaments(db=None):
    """
    This will delete a swiss tournament
    :param db:
    :return:
    """
    if not db:
        db = connect()
    sql_text="delete from SwissTournament"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def registerPlayer(name, db=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    if not db:
        db = connect()
    sql_text="select add_player('" + name +"')"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def playerStandings(tournament_id, db=None):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    if not db:
        db = connect()


    sql_text = "select * from get_player_standings(" + str(tournament_id) + ")"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()

    """
    At the start of the tournament we won't have any records in this table.
    We still want the standings.
    """
    if len(rows) == 0:
        sql_text="select id, username, 0 as wins, 0 as rounds from Players"
        cursor = db.cursor()
        cursor.execute(sql_text)
        prows = cursor.fetchall()
        for row in prows:
            rows.append(row)
    return rows

def reportMatch(winner, loser, tournamentid, current_round, db=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if not db:
        db = connect()

    sql_text = "select report_match(" + str(tournamentid) +"," + str(current_round) + "," + str(winner) + "," + str(loser) + ")"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def addPlayerForPairng(wins,player):

    if player[1] not in wins:
        list = []
        list.append(player)
        wins[player[1]] = list
    else:
        list = wins[player[1]]
        list.append(player)

def getSwissPairings(tournament_id, db, wins):
    """
    This will call a stored procedure to get the swiss pairings
    :param tournament_id:
    :param db:
    :param wins:
    :return:
    """
    sql_text = "select * from get_swiss_pairings(" + str(tournament_id) +")"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    for row in rows:
        addPlayerForPairng(wins,row)


def swissPairings(tournament_id, db=None,pastMatches=None):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    #sql_text="select winnerid, count(*) as wins from TournamentResults group by winnerid order by wins"
    if not db:
        db = connect()

    wins = dict()
    getSwissPairings(tournament_id, db, wins)
    if pastMatches:
        for win in wins:
            nomatch = NoMatch.NoRematch(wins,win,pastMatches)
            nomatch.get_no_rematch()
    pairing = 0
    count = 0
    swisspairing = []
    for win in wins:
        rows = wins[win]
        for row in rows:
            count +=1
            if count % 2 != 0:
                pairinglist = []
                pairinglist.append(row[0])
                pairinglist.append(row[2])
                swisspairing.append(pairinglist)
            else:
                pairinglist = swisspairing[pairing]
                pairinglist.append(row[0])
                pairinglist.append(row[2])
                pairing += 1

    return swisspairing



