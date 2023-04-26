from .connection import engine
from . import models

def create_db_tables():
    models.Base.metadata.create_all(bind=engine)
