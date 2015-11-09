"""
This is the SwissTournament module
It has a main class for running tournaments
"""
from random import randint
import tournament
import webbrowser
import os
def have_played_before(id1, id2, past_matches):
    """
    This just checks if players have played before.
    Really just a check to see if my logic is working.
    :param id1:
    :param id2:
    :param past_matches:
    :return:
    """
    for match in past_matches:
        if id1 == match[0] and id2 == match[1]:
            return True
        if id1 == match[1] and id2 == match[0]:
            return True
    return False

class SwissTournament(object):
    """
    This is the SwissTournament class
    It will run one or more tournament
    """

    def __init__(self, supportodd):
        """
        This is the constructor.  It takes one parameter if
        we will support odd lists
        :param supportodd:
        :return:
        """
        self.players = dict()
        self.swisspairing = []
        self.numplayers = None
        self.supportodd = supportodd
        self.database = tournament.connect()

    def load_players_from_file(self, filename):
        """
        This will load all the players from file and save them to the database
        :param filename:
        :return:
        """

        tournament.deletePlayers(self.database)
        players = open(filename, "r")
        for line in players:
            player = line.strip('\n')
            tournament.registerPlayer(player, self.database)
        players.close()

    def number_of_players(self):
        """
        This sets the number of players in the tournament
        :return:
        """
        players = tournament.countPlayers(self.database)
        print "Number of players " + str(players)
        self.numplayers = players

    def load_players_from_db(self):
        """
        This will load the players from the database and setup
        the first pairing. After this it will get them
        from the database
        :return:
        """

        del self.swisspairing[:]

        players = tournament.getPlayers(self.database)
        count = 0
        pairing = 0
        for player in players:
            if len(player) == 2:
                count += 1
                self.players[player[0]] = player[1]
                if count % 2 != 0:
                    pairinglist = []
                    pairinglist.append(player[0])
                    pairinglist.append(player[1])
                    self.swisspairing.append(pairinglist)
                else:
                    pairinglist = self.swisspairing[pairing]
                    pairinglist.append(player[0])
                    pairinglist.append(player[1])
                    pairing += 1

    def start_tournament(self, tournament_name):
        """
        This method is to start a new tournament.
        :param tournament_name:
        :return:
        """
        html_file = create_html_page(tournament_name)

        self.load_players_from_db()
        tournament.registerSwissTournament(tournament_name, self.database)
        tournament_id = tournament.getSwissTournamentId(tournament_name,
                                                        self.database)

        results = tournament.playerStandings(tournament_id, self.database)
        print_standings(results, 1)

        self.play_round(tournament_id, 1)
        tournament.updateSwissTournamentRound(tournament_id, 1, self.database)
        results = tournament.playerStandings(tournament_id, self.database)
        print_standings(results, 1)
        print_html_standings(html_file,results,1)

        past_matches = tournament.getPastMatchesForTournament(self.database,
                                                             tournament_id)
        self.swisspairing = tournament.swissPairings(tournament_id,
                                                    self.database,
                                                    past_matches)
        self.play_round(tournament_id, 2)
        tournament.updateSwissTournamentRound(tournament_id, 2, self.database)
        results = tournament.playerStandings(tournament_id, self.database)
        print_standings(results, 2)
        print_html_standings(html_file,results,2)

        past_matches = tournament.getPastMatchesForTournament(self.database,
                                                              tournament_id)
        self.swisspairing = tournament.swissPairings(tournament_id,
                                                     self.database,
                                                    past_matches)
        self.play_round(tournament_id, 3, past_matches)
        tournament.updateSwissTournamentRound(tournament_id, 3, self.database)
        results = tournament.playerStandings(tournament_id, self.database)
        print_standings(results, 3)
        print_html_standings(html_file,results,3)

        past_matches = tournament.getPastMatchesForTournament(self.database,
                                                              tournament_id)
        self.swisspairing = tournament.swissPairings(tournament_id,
                                                     self.database,
                                                    past_matches)
        self.play_round(tournament_id, 4, past_matches)
        tournament.updateSwissTournamentRound(tournament_id, 4, self.database)
        results = tournament.playerStandings(tournament_id, self.database)
        print_standings(results, 4)
        print_html_standings(html_file,results,4)

        html_file.write("</body>\n</html>\n")
        html_file.close()
        url = os.path.abspath(html_file.name)
        webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

    def play_round(self, tournament_id, current_round, past_matches=None):
        """
        This will play a given round in a tournament
        and report the match to the database.
        :param tournament_id:
        :param current_round:
        :return:
        """

        for pairings in self.swisspairing:
            if len(pairings) == 4:
                if past_matches:
                    if have_played_before(pairings[0], pairings[2],
                                          past_matches):
                        print "This pairing has played before pairings1=" \
                              + str(pairings[0]) \
                              + " pairings2=" + str(pairings[2])
                aval = randint(0, 9)
                bval = randint(0, 9)
                if aval > bval:
                    tournament.reportMatch(pairings[0], pairings[2],
                                           tournament_id, current_round,
                                           self.database)
                else:
                    tournament.reportMatch(pairings[2], pairings[0],
                                           tournament_id, current_round,
                                           self.database)

def create_html_page(tournament_name):

    filename = tournament_name + ".html";
    filename = filename.replace(' ', '')
    html_file = open(filename,"w")
    html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>" + tournament_name + "</title>\n</head>\n")
    html_file.write("<link href=\"stylesheet.css\" type=\"text/css\" rel=\"stylesheet\"")
    html_file.write("<body>\n<h1>" + tournament_name + "</h1>\n")
    return html_file

def print_html_standings(html_file, results, current_round):

    html_file.write("<h2>Round: " + str(current_round) + "</h2>\n")
    html_file.write("<table>\n")
    html_file.write("<tr>\n<th>ID</th>\n<th>NAME</th>\n<th>WINS</th>\n<th>ROUNDS</th>\n</tr>\n")
    for result in results:
        html_file.write("<tr>\n")
        html_file.write("<td>" + str(result[0]) + "</td>\n")
        html_file.write("<td>" + str(result[1]) + "</td>\n")
        html_file.write("<td>" + str(result[2]) + "</td>\n")
        html_file.write("<td>" + str(result[3]) + "</td>\n")
        html_file.write("</tr>\n")
    html_file.write("</table>\n")

def print_standings(results, current_round):
    """
    This will print the results for a given round
    based on the results passed in.
    :param results:
    :param round:
    :return:
    """
    print "Results for Round " + str(current_round)
    print "%5s %-20s %10s %10s" % ("id", "Name", "Wins", "Rounds")
    for result in results:
        print "%5d %-20s %10d %10d" % (result[0], result[1],
                                       result[2], result[3])

def main():
    """
    This is the main function that sets up the tournament
    :return:
    """
    myswiss = SwissTournament(False)
    tournament.deleteMatches(myswiss.database)
    tournament.deleteSwissTournaments(myswiss.database)
    myswiss.load_players_from_file("players.txt")
    myswiss.number_of_players()
    myswiss.start_tournament("Tournament One")
    myswiss.start_tournament("Tournament Two")

if __name__ == "__main__":
    main()
