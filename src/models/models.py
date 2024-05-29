from sqlalchemy import Table, Boolean, Column, Integer, String
from src.config.configDatabase import Base

class FilmModel(Base):
    __tablename__ = 'serie'
    id = Column(Integer, primary_key= True, index=True,autoincrement=True)
    name = Column(String(50))
    director = Column(String(100))
    urlPoster = Column(String(500))
    urlTrailer = Column(String(500))
    descripcion = Column(String(100))
    duration = Column(Integer)
    category = Column(String(20))
    



