from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
from psycopg2.extensions import parse_dsn
from flask_sqlalchemy import SQLAlchemy



conn = psycopg2.connect(
    host=os.environ.get('POSTGRES_HOST'),
    database=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    port=5432
    )

cur = conn.cursor()
database = SQLAlchemy()
