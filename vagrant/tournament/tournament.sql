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