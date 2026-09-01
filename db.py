import psycopg
from config import config


def get_connection():
    return psycopg.connect(**config)