from sqlalchemy import text
from app.db.session import engine

with engine.connect() as conn:
    res = conn.execute(text("SELECT 1")).scalar_one()
    print("DB OK: ", res)
