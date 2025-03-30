import pandas as pd
import sys
import os
from sqlalchemy import Column, Integer, String, Float, BigInteger, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import PrimaryKeyConstraint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()

class Sport(Base):
    __tablename__ = 't001_sports'
    __table_args__ = {'schema': 's002_silver'}
    
    sport = Column(String(100), primary_key=True)
    live = Column(Integer)
    total = Column(Integer)
    updated_at = Column(String(50))

class Country(Base):
    __tablename__ = 't002_countries'
    __table_args__ = {'schema': 's002_silver'}
    
    sport_country_id = Column(Integer, primary_key=True)
    sport = Column(String(100), ForeignKey('s002_silver.t001_sports.sport'))
    country_name = Column(String(100))
    updated_at = Column(String(50))

class Tournament(Base):
    __tablename__ = 't003_tournaments'
    __table_args__ = {'schema': 's002_silver'}

    tournament_id = Column(Integer, primary_key=True)
    tournament_name = Column(String(100), nullable=False)
    sport_country_id = Column(Integer, ForeignKey('s002_silver.t002_countries.sport_country_id'))
    category_name = Column(String(100))
    updated_at = Column(String(50))

    sport_country = relationship('Country')  # Corrigido o relacionamento

class Season(Base):
    __tablename__ = 't004_seasons'
    __table_args__ = {'schema': 's002_silver'}

    unique_tournament_id = Column(Integer, ForeignKey('s002_silver.t003_tournaments.tournament_id'))
    tournament_season_name = Column(String(100))
    season_year = Column(Integer)
    season_id = Column(Integer, primary_key=True)
    updated_at = Column(String(50))

class Round(Base):
    __tablename__ = 't005_rounds'
    __table_args__ = {'schema': 's002_silver'}
    
    season_id_round_slug = Column(String(100), primary_key=True)
    unique_tournament_id = Column(Integer)
    season_id = Column(Integer, ForeignKey('s002_silver.t004_seasons.season_id'))
    round = Column(Integer)
    slug = Column(String(100))
    updated_at = Column(String(50))

class Match(Base):
    __tablename__ = 't006_matches'
    __table_args__ = {'schema': 's002_silver'}
    
    match_id = Column(Integer, primary_key=True)
    season_id_round_slug = Column(String(100), ForeignKey('s002_silver.t005_rounds.season_id_round_slug'))
    unique_tournament_id = Column(Integer)
    season_id = Column(Integer)
    round = Column(Integer)
    slug = Column(String(100))
    tournament_name = Column(String(100))
    cup_round_type = Column(String(50))
    match_slug = Column(String(100))
    match_timestamp = Column(BigInteger)
    match_datatime = Column(String(50))
    home_team_id = Column(Integer)
    home_team_name = Column(String(100))
    home_score = Column(Float)
    away_score = Column(Float)
    away_team_name = Column(String(100))
    away_team_id = Column(Integer)

class MatchesStatistic(Base):
    __tablename__ = 't007_matches_statistics'
    __table_args__ = {'schema': 's002_silver'}
    
    match_id_key = Column(String(100), primary_key=True)
    match_id = Column(Integer, ForeignKey('s002_silver.t006_matches.match_id'))
    period = Column(String(100))
    groupname = Column(String(100))
    name = Column(String(100))
    home = Column(String(100))
    away = Column(String(100))
    statistics = Column(String(100))
    key = Column(String(100))

    match = relationship('Match')

class Lineup(Base):
    __tablename__ = 't008_lineups'
    __table_args__ = {'schema': 's002_silver'}
    
    match_id = Column(Integer, ForeignKey('s002_silver.t006_matches.match_id'))
    match_id_player_id = Column(BigInteger, primary_key=True)
    home_or_away = Column(String(50))
    formation = Column(String(50))
    player_id = Column(Integer)
    player_name = Column(String(100))
    player_slug = Column(String(100))
    list_country = Column(String(100))
    list_market_currency = Column(String(10))
    list_market_value = Column(Float)
    list_brithdate = Column(String(50))
    player_position = Column(String(50))
    player_number = Column(Float)
    player_substitute = Column(String(50))
    player_captain = Column(String(50))
    player_out_reason = Column(String(100))
    player_rating_sofascore = Column(Float)

    match = relationship('Match')

class LineupStatistic(Base):
    __tablename__ = 't009_lineups_statistics'
    __table_args__ = {'schema': 's002_silver'}
    
    match_id_player_id_statistic_name = Column(String(200), primary_key=True)
    match_id_player_id = Column(BigInteger, ForeignKey('s002_silver.t008_lineups.match_id_player_id'))
    match_id = Column(Integer)
    home_or_away = Column(String(50))
    formation = Column(String(50))
    player_id = Column(Integer)
    player_name = Column(String(100))
    player_slug = Column(String(100))
    list_player_country = Column(String(100))
    list_player_market_currency = Column(String(10))
    list_player_market_value = Column(Float)
    list_player_brithdate = Column(String(50))
    player_position = Column(String(50))
    player_number = Column(Float)
    player_substitute = Column(String(50))
    player_captain = Column(String(50))
    player_out_reason = Column(String(200))
    player_statistic_name = Column(String(100))
    player_statistic_value = Column(String(50))

    match = relationship('Match')

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)
