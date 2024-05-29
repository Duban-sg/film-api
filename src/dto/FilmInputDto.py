from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

class FilmInputDto():
    name: Annotated[str, Form()]
    director: Annotated[str, Form()]
    descripcion: Annotated[str, Form()]
    duration: Annotated[int, Form()]
    category: Annotated[str, Form()]
    poster: Annotated[UploadFile, File()]
    trailer: Annotated[UploadFile, File()]
    
    