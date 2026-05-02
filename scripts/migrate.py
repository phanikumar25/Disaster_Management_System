from __future__ import annotations

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, text

from src.world_model.models import create_schema


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set to run the world model migration.")

    engine = create_engine(database_url, pool_pre_ping=True)

    create_schema(engine)

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name IN ('zones', 'tasks', 'agents', 'inference_cache')
                ORDER BY table_name
                """
            )
        )
        for row in result:
            print(row.table_name)


if __name__ == "__main__":
    main()
