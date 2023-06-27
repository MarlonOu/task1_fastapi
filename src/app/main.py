from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models.Movies import Movies
from database.database import engine, Base, get_db
from repositories.MovieRepository import MovieRepository
from schemas.MoviesSchema import MovieRequest, MovieResponse
import controllers.MoviesController as Movies
import controllers.LoginController as Login
import controllers.UserController as User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Movies.movies)
app.include_router(Login.login)
app.include_router(User.user)
