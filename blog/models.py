from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


# SQL alchemy model


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    # back populates means need to add relationship to User as well
    # To establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one, specify an additional relationship() and connect the two using the relationship.back_populates parameter:
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="blogs")
