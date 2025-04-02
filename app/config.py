import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://local_user:##123##@localhost/local_user_db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
