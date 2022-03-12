import os
import environ  # type: ignore

_env = environ.Env()


#Database
DATABASE_HOST = _env('DATABASE_HOST')
DATABASE_NAME = _env('DATABASE_NAME')
DATABASE_USERNAME = _env('DATABASE_USERNAME')
DATABASE_PASSWORD = _env('DATABASE_PASSWORD')
