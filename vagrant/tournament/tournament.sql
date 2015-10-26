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