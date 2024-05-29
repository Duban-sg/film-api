from typing import Annotated,Union
from src.config.loadEnv import config
from src.config.configDatabase import Database
from fastapi import FastAPI, HTTPException, Depends, status, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.models import models
from src.config.awsS3 import awsS3

app = FastAPI()

db = Database(password=config["password"],username=config["username"],host=config["host"],database=config["database"],port=config["port"])
db.initDatabase()
db.initTable(models)

awsS3 = awsS3(AWS_ACCESS_KEY_ID=config["AWS_ACCESS_KEY"], AWS_SECRET_ACCESS_KEY=config["AWS_SECRET_ACCESS_KEY"],bucket=config["bucket"])
awsS3.connect()

db_dependency = Annotated[Session, Depends(db.get_db)]





@app.post("/api/v1/film/",response_model=None)
async def create_film(    name: Annotated[str, Form()],
    director: Annotated[str, Form()],
    descripcion: Annotated[str, Form()],
    duration: Annotated[int, Form()],
    category: Annotated[str, Form()],
    poster: Annotated[UploadFile, File()],
    trailer: Annotated[UploadFile, File()], db: db_dependency):
    try:
        urlPoster = awsS3.send_attachment(poster.file,name,poster.filename.split('.')[-1])
        urlTrailer = awsS3.send_attachment(trailer.file,name,trailer.filename.split('.')[-1])
        
        film = {
            "name": name,
            "director": director,
            "descripcion": descripcion,
            "duration": duration,
            "category": category,
            "urlPoster": urlPoster,
            "urlTrailer": urlTrailer
        }
        
        db_post = models.FilmModel(**film)
        db.add(db_post)
        db.commit()
        return "Created film"
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))

@app.get("/api/v1/film/")
async def getFilm(db: db_dependency):
    def mapResponse(f:models.FilmModel):
        f.urlPoster = awsS3.get_url_location_file(f.urlPoster)
        f.urlTrailer = awsS3.get_url_location_file(f.urlTrailer)
        return f
    try:
        films = db.query(models.FilmModel).all()
        films = [mapResponse(f) for f in films]
        return films
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))

    
@app.patch("/api/v1/pelicula/updateAttachment/{filmId}")
async def updateFile(filmId: str,file:Annotated[UploadFile, File()], atributeName: Annotated[str,""],db: db_dependency):
    try:
        film =  db.query(models.FilmModel).filter(models.FilmModel.id == filmId).first()
        attachmentName = ""
        if atributeName in ["urlPoster","urlTrailer"] :
            attachmentName = film.urlPoster if atributeName=="urlPoster" else film.urlTrailer
        else:
            raise Exception("Invalid attribute")
        fleName = awsS3.update_attachment(file.file,attachmentName)
        
        if atributeName=="urlPoster":
            film.urlPoster = fleName
        else:
            film.urlTrailer = fleName
        db.flush()
        return awsS3.get_url_location_file(fleName)
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))



