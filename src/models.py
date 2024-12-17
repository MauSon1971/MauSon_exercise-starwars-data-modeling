import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla intermedia para la relación muchos-a-muchos entre Usuarios y Planetas favoritos
favorite_planet_table = Table(
    'favorite_planet',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('planet_id', Integer, ForeignKey('planets.id'))
)

# Tabla intermedia para la relación muchos-a-muchos entre Usuarios y Personajes favoritos
favorite_people_table = Table(
    'favorite_people',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('character_id', Integer, ForeignKey('characters.id'))
)

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String)

    # Relación con planetas y personanjes favoritos
    favorite_planets = relationship("Planets", secondary=favorite_planet_table, back_populates="favorited_by_users")
    favorite_characters = relationship("Characters", secondary=favorite_people_table, back_populates="favorited_by_users")

    def __repr__(self):
        return f"<User {self.username}>"

class Characters(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    homeworld_id = Column(Integer, ForeignKey('planets.id'))  # FK a Planetas
    url = Column(String)

    # Relación inversa con Planet (un planeta puede tener múltiples personajes)
    homeworld = relationship("Planets", back_populates="residents")

    # Relación con usuarios (favoritos)
    favorited_by_users = relationship("User", secondary=favorite_people_table, back_populates="favorite_characters")

    def __repr__(self):
        return f"<Character {self.name}>"

class Planets(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)

    # Relación inversa con Characters (residentes del planeta)
    residents = relationship("Characters", back_populates="homeworld")

    # Relación con usuarios (favoritos)
    favorited_by_users = relationship("User", secondary=favorite_planet_table, back_populates="favorite_planets")

    def __repr__(self):
        return f"<Planet {self.name}>"

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
