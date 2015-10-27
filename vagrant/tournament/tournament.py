#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


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

    sql_text="select * from Players"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    return rows

def registerSwissTournament(name, db=None):

    if not db:
        db = connect()
    sql_text="insert into SwissTournament(name,rounds) values('" + name +"',0)"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def getSwissTournamentId(name, db=None):

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

    if not db:
        db = connect()
    sql_text="Update SwissTournament set rounds=" + str(round) + " where id=" + str(tournament_id)
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

def deleteSwissTournaments(db=None):

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
    sql_text="insert into Players(username) values('" + name +"')"
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

    sql_text = "select tr.winnerid, p.username, count(*) as wins, st.rounds  from TournamentResults tr, Players p, SwissTournament st"
    sql_text += " where tr.winnerid=p.id and st.id=" + str(tournament_id) + " and tr.tournamentid=st.id"
    sql_text += " group by tr.winnerid, p.username, st.rounds order by wins desc"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()

    sql_text = "select distinct tr.loserid, p.username, 0 as wins, st.rounds from TournamentResults tr, Players p, SwissTournament st"
    sql_text += " where tr.loserid=p.id and st.id=" + str(tournament_id) + " and tr.tournamentid=st.id and "
    sql_text += "tr.loserid not in(select distinct winnerid from TournamentResults)"
    cursor = db.cursor()
    cursor.execute(sql_text)
    lrows = cursor.fetchall()
    for row in lrows:
        rows.append(row)
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
    sql_text = "insert into TournamentResults(tournamentId,round,winnerId,loserId) values("
    sql_text += str(tournamentid) +"," + str(current_round) + "," + str(winner) + "," + str(loser) + ")"
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()

 
def swissPairings(db=None):
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
    sql_text = "select tr.winnerid, count(*) as wins, p.username  from TournamentResults tr, Players p where tr.winnerid=p.id"
    sql_text += " group by tr.winnerid, p.username order by wins desc"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    pairing = 0
    count = 0
    swisspairing = []
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

    sql_text = "select distinct tr.loserid,p.username from TournamentResults tr, Players p where tr.loserid=p.id and "
    sql_text += "tr.loserid not in(select distinct winnerid from TournamentResults)"
    cursor = db.cursor()
    cursor.execute(sql_text)
    rows = cursor.fetchall()
    for row in rows:
        count +=1
        if count % 2 != 0:
            pairinglist = []
            pairinglist.append(row[0])
            pairinglist.append(row[1])
            swisspairing.append(pairinglist)
        else:
            pairinglist = swisspairing[pairing]
            pairinglist.append(row[0])
            pairinglist.append(row[1])
            pairing += 1

    return swisspairing



