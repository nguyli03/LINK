from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, create_engine, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import os

# f = open('app/server/.env','r')
# content = f.readline().split('=')[1].strip('\n')
# os.environ['DATABASE_URL'] = content
# f.close()

postgresql_uri=os.environ['DATABASE_URL']
engine=create_engine(postgresql_uri)

Session = sessionmaker(bind=engine)
db = Session()
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
def createTables():
    # delete the tables, just for this test:
    # db.execute('drop table unavailability; drop table shift; drop table student; drop table manager; drop table department;')
    # Create tables if not exists
    # db.execute("DROP table shift;")
    # db.execute("DROP table unavailability;")
    db.execute("""CREATE table if not exists users(\
                            username text not null,\
                            password text not null);""")

    db.execute("""CREATE table if not exists favRecipes(\
                                username text not null,\
                                recipe text not null);""")
    db.commit()
