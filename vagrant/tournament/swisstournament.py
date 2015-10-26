"""
This is the SwissTournament module
It has a main class for running tournaments
"""
from random import randint
import tournament

class SwissTournament(object):
    """
    This is the SwissTournament class
    It will run one or more tournament
    """

    def __init__(self, supportodd):
        """
        This is the constructor.  It takes one parameter if we will support odd lists
        :param supportodd:
        :return:
        """
        self.players = dict()
        self.swisspairing = []
        self.numplayers = None
        self.supportodd = supportodd
        self.db = tournament.connect()

    def load_players_from_file(self,filename):
        """
        This will load all the players from file and save them to the database
        :param filename:
        :return:
        """

        tournament.deletePlayers(self.db)
        players = open(filename,"r")
        for line in players:
            player = line.strip('\n');
            tournament.registerPlayer(player,self.db)
        players.close()

    def number_of_players(self):
        """
        This sets the number of players in the tournament
        :return:
        """
        players = tournament.countPlayers(self.db)
        print "Number of players " + str(players[0])
        self.numplayers = players[0]

    def load_players_from_db(self):
        """
        This will load the players from the database and setup the first pairing.
        After this it will get them from the database
        :return:
        """

        numpairings = int(self.numplayers/2) + (self.numplayers%2)

        players = tournament.getPlayers(self.db)
        count = 0
        pairing = 0
        for player in players:
            if len(player) == 2:
                count += 1
                self.players[player[0]] = player[1]
                if count % 2 != 0:
                    pairinglist = []
                    playerlist = []
                    playerlist.append(player[0])
                    playerlist.append(player[1])
                    pairinglist.append(playerlist)
                    self.swisspairing.append(pairinglist)
                else:
                    pairinglist = self.swisspairing[pairing]
                    playerlist = []
                    playerlist.append(player[0])
                    playerlist.append(player[1])
                    pairinglist.append(playerlist)
                    pairing += 1

    def play_round(self, tournament_id,current_round):
        """
        This will play a given round in a tournament and report the match to the database.
        :param tournament_id:
        :param current_round:
        :return:
        """

        for parings in self.swisspairing:
            if len(parings) == 2:
                aval = randint(0,9)
                bval = randint(0,9)
                if aval > bval:
                    tournament.reportMatch(parings[0][0],parings[1][0],tournament_id,current_round,self.db)
                else:
                    tournament.reportMatch(parings[1][0],parings[0][0],tournament_id,current_round,self.db)

def printStandings(results, round):
    """
    This will print the results for a given round based on the results passed in.
    :param results:
    :param round:
    :return:
    """
    print "Results for Round " + str(round)
    print("%5s %-20s %10s %10s" % ("id","Name","Wins","Rounds"))
    for result in results:
        print("%5d %-20s %10d %10d" % (result[0], result[2], result[1], result[3]))

def main():
    """
    This is the main function that sets up the tournament
    :return:
    """
    myswiss = SwissTournament(False)
    tournament.deleteMatches(myswiss.db,1)
    tournament.deleteSwissTournaments(myswiss.db)
    myswiss.load_players_from_file("players.txt")
    myswiss.number_of_players()
    myswiss.load_players_from_db()
    tournament.registerSwissTournament(myswiss.db,"Test Tournament")
    tournament_id = tournament.getSwissTournamentId(myswiss.db,"Test Tournament")
    myswiss.play_round(tournament_id,1)
    tournament.updateSwissTournamentRound(myswiss.db,tournament_id,1)
    results= tournament.playerStandings(myswiss.db,tournament_id)
    printStandings(results,1)

    myswiss.swisspairing = tournament.swissPairings(myswiss.db)
    myswiss.play_round(tournament_id,2)
    tournament.updateSwissTournamentRound(myswiss.db,tournament_id,2)
    results= tournament.playerStandings(myswiss.db,tournament_id)
    printStandings(results,2)

    myswiss.swisspairing = tournament.swissPairings(myswiss.db)
    myswiss.play_round(tournament_id,3)
    results= tournament.playerStandings(myswiss.db,tournament_id)
    printStandings(results,3)

    tournament.updateSwissTournamentRound(myswiss.db,tournament_id,3)
    myswiss.swisspairing = tournament.swissPairings(myswiss.db)
    myswiss.play_round(tournament_id,4)
    tournament.updateSwissTournamentRound(myswiss.db,tournament_id,4)
    results= tournament.playerStandings(myswiss.db,tournament_id)
    printStandings(results,4)

if __name__ == "__main__":
    main()