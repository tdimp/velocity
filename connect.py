import psycopg
from config import config

with psycopg.connect(**config) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version()")
        print(cur.fetchone())