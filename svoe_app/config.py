import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:0000@localhost:5433/svoe_db')