#!/usr/bin/python3
""" New engine DBStorage """
import sqlalchemy
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os

classes = {
    # 'BaseModel': BaseModel,
    'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """ DBStorage Class """
    __engine = None
    __session = None

    def __init__(self):
        """initialize object"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')

        self.__engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'
            .format(user,
                    password,
                    host,
                    database), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == "test":
            # from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all method """
        dict_objs = {}
        if cls:
            for name in classes:
                if cls.__name__ == name:
                    find = self.__session.query(classes[name]).all()
                    for i in find:
                        key = i.__class__.__name__ + '.' + i.id
                        dict_objs[key] = i
        elif cls is None:
            for name in classes:
                find = self.__session.query(classes[name]).all()
                for i in find:
                    key = i.__class__.__name__ + '.' + i.id
                    dict_objs[key] = i
        return dict_objs

    def new(self, obj):
        """ new method """
        self.__session.add(obj)

    def save(self):
        """ save method """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete method """
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """ reload method """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session()

    # def close(self):
    #     """ close method """
    #     self.reload(remove=True)
