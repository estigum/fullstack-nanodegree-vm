"""
This module is used to make sure we don't
have any rematches if the user choses to enfore
tht
"""
def have_played_before(id1, id2, past_matches):
    """
    This will see if two players have already matched up
    :param id1:
    :param id2:
    :param past_matches:
    :return True if they have or False if they have not:
    """
    for match in past_matches:
        if id1 == match[0] and id2 == match[1]:
            return True
        if id1 == match[1] and id2 == match[0]:
            return True
    return False

def get_player(player_id, match_list):
    """
    This will get the player from the list fro a given id
    :param id:
    :param list:
    :return the player or None if you can't find it:
    """
    for player in match_list:
        if player_id == player[0]:
            return player
    return None

def is_in_player_list(match_list, player):
    """
    This will see if this player has already been added
    to the player list
    :param list:
    :param player:
    :return if True they have.  If False no:
    """
    for item in match_list:
        if player[0] == item[0]:
            return True
    return False

def get_min_good_match(good_match):
    """
    This will get the minimum number of good matches.
    Reason for that is these are the ones that are going to
    have the hardest time matching up.
    :param good_match:
    :return minum size of good matches:
    """
    count = -1
    for next_id in good_match:
        good_list = good_match[next_id]
        if count == -1 or len(good_list) < count:
            count = len(good_list)

    return count

def get_max_good_match(good_match):
    """
    This will get the maximum of good matches
    These are the ones we process last
    :param good_match:
    :return return the max of the good_match collection:
    """
    count = 0
    for next_id in good_match:
        good_list = good_match[next_id]
        if len(good_list) > count:
            count = len(good_list)

    return count

def get_next_good_match_id(count, id_list, good_match):
    """
    This will get the next good match id for a given size of the list.
    If it can't find anymore then we will increment
    :param count:
    :param id_list:
    :param good_match:
    :return The id or None:
    """

    for tid in good_match:
        good_list = good_match[tid]
        if tid not in id_list and len(good_list) == count:
            return tid
    return None

class NoRematch(object):
    """
    This class will prevent any to players from
    playing once
    """

    def __init__(self, wins, win, past_matches):
        """
        This is the contructor
        :param wins:
        :param win:
        :param past_matches:
        :return:
        """
        self.wins = wins
        self.win = win
        self.past_matches = past_matches


    def get_good_had_match(self):
        """
        This will return the matches a given player has had
        and the ones that they have not yet had
        :return ones matched up and ones not:
        """
        had_match = dict()
        good_match = dict()
        match_list = self.wins[self.win]
        for player in match_list:
            had_match[player[0]] = []
            good_match[player[0]] = []
            for tplayer in match_list:
                if player[0] != tplayer[0]:
                    if have_played_before(player[0], tplayer[0],
                                          self.past_matches):
                        tlist = had_match[player[0]]
                        tlist.append(tplayer[0])
                    else:
                        tlist = good_match[player[0]]
                        tlist.append(tplayer[0])
        return had_match, good_match



    def get_no_rematch(self):
        """
        This will get all the matchups that are
        not rematches.
        :return Nothing:
        """
        had_match, good_match = self.get_good_had_match()
        min_val = get_min_good_match(good_match)
        max_val = get_max_good_match(good_match)
        count = min_val
        id_list = []
        ret_list = []
        match_list = self.wins[self.win]
        matched = False
        while count <= max_val:
            next_id = get_next_good_match_id(count, id_list, good_match)
            id_list.append(next_id)
            if next_id:
                player = get_player(next_id, match_list)
                if is_in_player_list(ret_list, player):
                    continue
                ret_list.append(player)
                bad_match = had_match[next_id]
                if len(bad_match) > 0:
                    for tid in had_match:
                        tbad_match = had_match[tid]
                        if tid != next_id and len(tbad_match) > 0:
                            tplayer = get_player(tid, match_list)
                            if tid not in bad_match and \
                                    not is_in_player_list(ret_list, tplayer):
                                ret_list.append(tplayer)
                                matched = True
                                break
                if matched:
                    matched = False
                    continue
                tlist = good_match[next_id]
                for tid in tlist:
                    tplayer = get_player(tid, match_list)
                    if not is_in_player_list(ret_list, tplayer):
                        ret_list.append(tplayer)
                        break
            else:
                count += 1

        self.wins[self.win] = ret_list
