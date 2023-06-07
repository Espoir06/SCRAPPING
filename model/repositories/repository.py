from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

class Repository():
    def get_engine():
        return create_engine(f'mysql+mysqlconnector://espoir:espoir123@localhost/projetPython')
    
    def connect():
        engine = Repository.get_engine()
        Repository.Session = scoped_session(sessionmaker(bind=engine))
        
    def disconnect():
        Repository.Session.remove()
        
    def store(table):
        Repository.Session.add(table)
        Repository.Session.commit()
        return table
    
    def update(table):
        Repository.Session.commit()
        return table
    
    def delete(table):
        print(table)
        Repository.Session.delete(table)
        Repository.Session.commit()