-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--This is the Players table that contains all the players in the tournaments
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

DROP TABLE IF EXISTS Players;
CREATE TABLE Players(
id serial,
username varchar(30),
PRIMARY KEY(id));

--The SwissTournament contains all the tournaments that are going on.
DROP TABLE IF EXISTS SwissTournament;
CREATE TABLE SwissTournament(
id serial,
name varchar(30),
rounds int,
PRIMARY KEY(id));

--TournamentResults contains the results for a specific tournament based on the tournamentid.
DROP TABLE IF EXISTS TournamentResults;
CREATE TABLE TournamentResults(
tournamentId int,
round int,
winnerId int,
loserId int);

--update_tournament_round. This stored procedure will update the current round for a tournament
DROP FUNCTION update_tournament_round(_round int, _tournamentid int);
CREATE FUNCTION update_tournament_round(_round int, _tournamentid int) returns void
    AS $$
    BEGIN
      UPDATE SwissTournament set rounds=_round where id=_tournamentid;
    END;
    $$ LANGUAGE PLPGSQL VOLATILE
    COST 100;

--add_player.  This stored procedure will add a player
DROP FUNCTION add_player(_pname varchar);
CREATE FUNCTION add_player(_pname varchar) returns void
    AS $$
    BEGIN
        insert into Players(username) values(_pname);
    END;
    $$ LANGUAGE PLPGSQL VOLATILE
    COST 100;

--register_swiss_tournament. This will add another tournament
DROP FUNCTION register_swiss_tournament(_name varchar);
CREATE or REPLACE FUNCTION register_swiss_tournament(_name varchar) returns void
    AS $$
    BEGIN
        insert into SwissTournament(name,rounds) values(_name,0);
    END;
    $$ LANGUAGE PLPGSQL VOLATILE
    COST 100;

--report_match.  this will report a match that happened.
DROP FUNCTION report_match(_tournamentid int , _round int, _winner int, _loser int);
CREATE or REPLACE FUNCTION report_match(_tournamentid int , _round int, _winner int, _loser int) returns void
    AS $$
    BEGIN
        insert into TournamentResults(tournamentId,round,winnerId,loserId) values(_tournamentid,_round,_winner,_loser);
    END;
    $$ LANGUAGE PLPGSQL VOLATILE
    COST 100;

--get_past_matches - This will get past matches
DROP FUNCTION get_past_matches(_tournamentid int);
CREATE FUNCTION get_past_matches(_tournamentid int)
    RETURNS TABLE (winnerid int,
                   loserid int)
    AS $$
    BEGIN
        RETURN QUERY select tr.winnerid as winnerid,
                            tr.loserid as loserid
                            from TournamentResults tr
                            where tr.tournamentid=_tournamentid
                            and tr.loserid != 0;
    END;
    $$ LANGUAGE PLPGSQL;

--get_player_standings.  This will get the current standings.
DROP FUNCTION get_player_standings(tourId int);
CREATE or REPLACE FUNCTION get_player_standings(tourId int)
   RETURNS TABLE (userid int,
                  username varchar(30),
                  wins bigint,
                  round int)
    AS $$
    DECLARE
      num_tournament int;
    BEGIN
      select count(*) into num_tournament as num_tournament from SwissTournament;
      num_tournament := num_tournament * 4;
      IF tourId >0 THEN
        RETURN QUERY select
                   tr.winnerid as userid,
                   p.username as username,
                   count(*) as wins,
                   st.rounds as round
                   from TournamentResults tr, Players p, SwissTournament st
                   where tr.winnerid = p.id and st.id = tourId and tr.tournamentid = st.id
                   group by tr.winnerid, p.username, st.rounds order by wins desc;
       ELSE
        RETURN QUERY select
                   tr.winnerid as userid,
                   p.username as username,
                   count(*) as wins,
                   num_tournament as round
                   from TournamentResults tr, Players p, SwissTournament st
                   where tr.winnerid = p.id and tr.tournamentid = st.id
                   group by tr.winnerid, p.username, st.rounds order by wins desc;
      END IF;

      IF tourId >0 THEN
        RETURN QUERY select
                  distinct tr.loserid as userid,
                  p.username as username,
                  CAST(0 AS BIGINT) as wins,
                  st.rounds as round
                  from TournamentResults tr, Players p, SwissTournament st
                  where tr.loserid = p.id and st.id = tourId and tr.tournamentid = st.id and
                  tr.loserid not in(select distinct winnerid from TournamentResults where tournamentid= tourId)
                  and tr.loserid != -1
                  group by tr.loserid, p.username, st.rounds;
      ELSE
        RETURN QUERY select
                  distinct tr.loserid as userid,
                  p.username as username,
                  CAST(0 AS BIGINT) as wins,
                  num_tournament as round
                  from TournamentResults tr, Players p, SwissTournament st
                  where tr.loserid = p.id and  tr.tournamentid = st.id and
                  tr.loserid not in(select distinct winnerid from TournamentResults)
                  and tr.loserid != -1
                  group by tr.loserid, p.username, st.rounds;
      END IF;
    END;
    $$ LANGUAGE PLPGSQL;

--get_swiss_pariings - This will get the pairings for the next round.
DROP FUNCTION get_swiss_pairings(tourId int);
CREATE or REPLACE FUNCTION get_swiss_pairings(tourId int)
   RETURNS TABLE (userid int,
                  wins bigint,
                  username varchar(30))
    AS  $$
    BEGIN
      RETURN QUERY select
                   tr.winnerid as userid,
                   count(*) as wins,
                   p.username as username
                   from TournamentResults tr, Players p where
                   tr.tournamentid = tourId and tr.winnerid = p.id
                   group by tr.winnerid, p.username order by wins desc;
      RETURN QUERY select
                   distinct tr.loserid,
                   CAST(0 AS BIGINT) as wins,
                   p.username
                   from TournamentResults tr, Players p
                   where tr.tournamentid = tourId and tr.loserid = p.id and
                   tr.loserid not in(select distinct winnerid from TournamentResults where tournamentid = tourId)
                   and tr.loserid != -1
                   group by tr.loserid, p.username;
    END;
    $$ LANGUAGE PLPGSQL;