from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models.Movies import Movies
from database.database import engine, Base, get_db
from repositories.MovieRepository import MovieRepository
from schemas.MoviesSchema import MovieRequest, MovieResponse
import controllers.MoviesController as MoviesController

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(MoviesController.movies)
