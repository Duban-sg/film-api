from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database ():
    
    URL_DATABASE = "mysql+mysqlconnector://"
    engine = None
    Sessionlocal = None
    
    def __init__ (self,username=None,password=None,host=None,port=None,database=None):
        self.URL_DATABASE = self.URL_DATABASE+username+":"+password+""+"@"+host+":"+port+"/"+database
        
    def initDatabase (self):
        try:
            self.engine = create_engine(self.URL_DATABASE, pool_size= 10, max_overflow= 30)
            self.Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind= self.engine)
        except Exception as e:
            print("[ERROR]: Database initialization = "+str(e))

    def initTable (self, models):
        try:
            models.Base.metadata.create_all(bind = self.engine)
        except Exception as e:
            print("[ERROR]: Table initialization table = "+str(e))
    
    def get_db(self):
        db = self.Sessionlocal()
        try: 
            yield db

        finally:
            db.close()
        
    
    