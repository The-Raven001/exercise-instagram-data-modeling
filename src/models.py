import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er
from enum import Enum as PyEnum

Base = declarative_base()

class Type(PyEnum):
    PNG = ".png"
    JPEG = ".jpeg"
    WEBP = ".webp"


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    phone_number = Column(String(20), unique=True)
    bio = Column(String(500))

    is_active = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=True)

    follower = relationship('Follower', backref='followers')

class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    follower_id = Column(Integer, ForeignKey("user.id"))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(250), unique=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post)
    role = Column(SqlEnum(Type), nullable=False)

class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('user'))
    user = relationship(User)
    post_id = Column(Integer, ForeignKey('post'))
    post = relationship(Post)



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
