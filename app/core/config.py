import os
from dotenv import load_dotenv

load_dotenv()

ENV           = os.getenv("ENV", "dev")
SUPABASE_URL  = os.getenv("SUPABASE_URL")
SUPABASE_KEY  = os.getenv("SUPABASE_KEY")
SQLITE_PATH   = os.getenv("SQLITE_PATH", "./database/sqlite/geo.db")
