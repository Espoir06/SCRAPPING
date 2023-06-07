#!../.venv/bin/python3
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists
from models import Model

engine= create_engine(f'mysql+mysqlconnector://espoir:espoir123@localhost/projetPython')
#Session = sessionmaker(bind=engine)

# Vérifier si la base de données existe, sinon la créer
if not database_exists(engine.url):
    create_database(engine.url)

# Configurer les mappers pour la relation avec d'autres entités
configure_mappers()

# Effectuer la migration en créant les tables dans la base de données
Model.metadata.create_all(engine)
print(("Migrations effectué"))
