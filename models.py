# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import bson
from pymongo import MongoClient
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)

"""
SQLite Models. Database 1
"""
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand_id = Column(String)
    year = Column(Integer)


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    color = Column(String)
    model_id = Column(Integer, ForeignKey('models.id'))

    model = relationship(
        Model,
        backref=backref('models',
                        uselist=True,
                        cascade='delete,all'))


def get_model(info, id):
    from schema import Model as ModelSchema
    model = ModelSchema.get_query(info)
    return [f for f in model.filter_by(brand_id=id)]


"""
MongoDB Models. Database 2
"""

client = MongoClient('127.0.0.1', 28000)

db = client.factory

brands = db.brands


def get_brand(id):
    from schema import Brand
    result = brands.find_one({"_id": bson.ObjectId(str(id))})
    brand = Brand(id=str(result["_id"]), name=str(result["name"]))
    return brand


def get_brands():
    return [get_brand(i["_id"]) for i in brands.find()]
