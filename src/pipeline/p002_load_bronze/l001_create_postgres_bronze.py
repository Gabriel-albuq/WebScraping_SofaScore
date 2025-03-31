import sys
import os
from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.orm import declarative_base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()

class Sports(Base):
    __tablename__ = 't001_sports'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class Countries(Base):
    __tablename__ = 't002_countries'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class Tournaments(Base):
    __tablename__ = 't003_tournaments'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class Seasons(Base):
    __tablename__ = 't004_seasons'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)
    
class Rounds(Base):
    __tablename__ = 't005_rounds'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class Matches(Base):
    __tablename__ = 't006_matches'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class MatchesStatistics(Base):
    __tablename__ = 't007_matches_statistics'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class Lineups(Base):
    __tablename__ = 't008_lineups'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class LineupsStatistics(Base):
    __tablename__ = 't009_lineups_statistics'
    __table_args__ = {'schema': 's001_bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)
