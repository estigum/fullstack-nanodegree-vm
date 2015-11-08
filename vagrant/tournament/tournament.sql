-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS Players;
CREATE TABLE Players(
id serial,
username varchar(30),
PRIMARY KEY(id));

DROP TABLE IF EXISTS SwissTournament;
CREATE TABLE SwissTournament(
id serial,
name varchar(30),
rounds int,
PRIMARY KEY(id));

DROP TABLE IF EXISTS TournamentResults;
CREATE TABLE TournamentResults(
tournamentId int,
round int,
winnerId int,
loserId int);

DROP FUNCTION add_player(playername varchar);
CREATE FUNCTION add_player(_pname varchar) returns void
    AS $$
    BEGIN
        insert into Players(username) values(_pname);
    END;
    $$ LANGUAGE PLPGSQL VOLATILE
    COST 100;

DROP FUNCTION get_player_standings(tourId int);
CREATE or REPLACE FUNCTION get_player_standings(tourId int)
   RETURNS TABLE (userid int,
                  username varchar(30),
                  wins bigint,
                  round int)
    AS $$
    BEGIN
      RETURN QUERY select
                   tr.winnerid as userid,
                   p.username as username,
                   count(*) as wins,
                   st.rounds as round
                   from TournamentResults tr, Players p, SwissTournament st
                   where tr.winnerid = p.id and st.id = tourId and tr.tournamentid = st.id
                   group by tr.winnerid, p.username, st.rounds order by wins desc;

     RETURN QUERY select
                  distinct tr.loserid as userid,
                  p.username as username,
                  CAST(0 AS BIGINT) as wins,
                  st.rounds as round
                  from TournamentResults tr, Players p, SwissTournament st
                  where tr.loserid = p.id and st.id = tourId and tr.tournamentid = st.id and
                  tr.loserid not in(select distinct winnerid from TournamentResults where tournamentid= tourId)
                  group by tr.loserid, p.username, st.rounds;
    END;
    $$ LANGUAGE PLPGSQL;


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
                   group by tr.loserid, p.username;
    END;
    $$ LANGUAGE PLPGSQL;