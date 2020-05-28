import datetime
from sqlalchemy import create_engine, ForeignKey, Sequence, CheckConstraint
from sqlalchemy import Column, Date, Integer, String, Boolean, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{host}:{port}/{sid}'

engine = create_engine(
    oracle_connection_string.format(

        username="SYSTEM",
        password="oracle",
        sid="XE",
        host="localhost",
        port="1521",
        database="PROJECT",

    )
    , echo=True
)


Base = declarative_base()



class user_database (Base):
    __tablename__ = 'user_database'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    user_name = Column(String(100), nullable=False)
    user_mail = Column(String(100), nullable=False, unique=True)	
    user_age = Column(Integer, CheckConstraint('user_age >= 16'), nullable=False)
    login = Column(String(100), CheckConstraint('LENGTH(login) >= 5'), nullable=False, unique=True)
    user_pass = Column(String(100), CheckConstraint('LENGTH(user_pass) >= 5'), nullable=False)
    todolist = relationship('todolist', backref = 'todolist')
    
    def __init__(self, user_name, user_mail, user_age, login, user_pass):
        """"""
        self.user_name = user_name
        self.user_mail = user_mail
        self.user_age = user_age
        self.login = login
        self.user_pass = user_pass


class todolist (Base):
    __tablename__ = 'todolist'

    user_id = Column(Integer, ForeignKey('user_database.id'), primary_key= True )
    todolist_name = Column(String(100))
    description_of_todo = Column(String(200))
    time_creating = Column(TIMESTAMP, nullable=False, primary_key= True )
    status = Column(Boolean, nullable=False)

    def __init__(self, user_id, todolist_name, description_of_todo, time_creating, status):
        """"""
        self.user_id = user_id
        self.todolist_name = todolist_name
        self.description_of_todo = description_of_todo
        self.time_creating = time_creating
        self.status = status


# create tables
Base.metadata.create_all(engine)