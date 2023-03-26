#!/usr/bin/python3
""" Database Storage module """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base


class DBStorage:
    """ Fatabase Storage """
    __engine = None
    __Session = None
    
    def __init__(self):
        """ Initialize an instance of DBStorage """
        mysql_user = os.environ.get("HBNB_MYSQL_USER")
        mysql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        mysql_host = os.environ.get("HBNB_MYSQL_HOST", "localhost")
        mysql_db = os.environ.get("HBNB_MYSQL_DB")
        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}:3306/{}".format(mysql_user, mysql_pwd, mysql_host, mysql_db), pool_pre_ping=True)
        if os.environ.get("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.engine)

    def all(self, cls=None):
        """ Query on current database session """
        obj_dict = {}
        if cls:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            for cls in Base.__subclasses__():
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current database session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        DBStorage.__session = scoped_session(session_factory)
